import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.DecimalFormat;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class SentiWordNet {
	private final static String rootDir = "classification_output/";
	private Map<String, Double> dictionary;

	public SentiWordNet(String pathToSWN) throws IOException {
		// This is our main dictionary representation
		dictionary = new HashMap<String, Double>();

		// From String to list of doubles.
		HashMap<String, HashMap<Integer, Double>> tempDictionary = new HashMap<String, HashMap<Integer, Double>>();

		BufferedReader csv = null;
		try {
			csv = new BufferedReader(new FileReader(pathToSWN));
			int lineNumber = 0;

			String line;
			while ((line = csv.readLine()) != null) {
				lineNumber++;

				// If it's a comment, skip this line.
				if (!line.trim().startsWith("#")) {
					// We use tab separation
					String[] data = line.split("\t");
					String wordTypeMarker = data[0];

					// Example line:
					// POS ID PosS NegS SynsetTerm#sensenumber Desc
					// a 00009618 0.5 0.25 spartan#4 austere#3 ascetical#2
					// ascetic#2 practicing great self-denial;...etc

					// Is it a valid line? Otherwise, through exception.
					if (data.length != 6) {
						throw new IllegalArgumentException(
								"Incorrect tabulation format in file, line: "
										+ lineNumber);
					}

					// Calculate synset score as score = PosS - NegS
					Double synsetScore = Double.parseDouble(data[2])
							- Double.parseDouble(data[3]);

					// Get all Synset terms
					String[] synTermsSplit = data[4].split(" ");

					// Go through all terms of current synset.
					for (String synTermSplit : synTermsSplit) {
						// Get synterm and synterm rank
						String[] synTermAndRank = synTermSplit.split("#");
						String synTerm = synTermAndRank[0] + "#"
								+ wordTypeMarker;

						int synTermRank = Integer.parseInt(synTermAndRank[1]);
						// What we get here is a map of the type:
						// term -> {score of synset#1, score of synset#2...}

						// Add map to term if it doesn't have one
						if (!tempDictionary.containsKey(synTerm)) {
							tempDictionary.put(synTerm,
									new HashMap<Integer, Double>());
						}

						// Add synset link to synterm
						tempDictionary.get(synTerm).put(synTermRank,
								synsetScore);
					}
				}
			}

			// Go through all the terms.
			for (Map.Entry<String, HashMap<Integer, Double>> entry : tempDictionary
					.entrySet()) {
				String word = entry.getKey();
				Map<Integer, Double> synSetScoreMap = entry.getValue();

				// Calculate weighted average. Weigh the synsets according to
				// their rank.
				// Score= 1/2*first + 1/3*second + 1/4*third ..... etc.
				// Sum = 1/1 + 1/2 + 1/3 ...
				double score = 0.0;
				double sum = 0.0;
				for (Map.Entry<Integer, Double> setScore : synSetScoreMap
						.entrySet()) {
					score += setScore.getValue() / (double) setScore.getKey();
					sum += 1.0 / (double) setScore.getKey();
				}
				score /= sum;

				dictionary.put(word, score);
			}
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if (csv != null) {
				csv.close();
			}
		}
	}

	// Find sentiword score from map, go through parts of speech in adjective, noun, verb order
	// If the word isn't found, return -100 which will be handled later
	public double extract(String word) {
		if (dictionary.get(word + "#a") != null) {
			return dictionary.get(word + "#a");
		} else if (dictionary.get(word + "#n") != null) {
			return dictionary.get(word + "#n");
		} else if (dictionary.get(word + "#v") != null) {
			return dictionary.get(word + "#v");
		} else {
			return -100;
		}
	}

	public static void main(String[] args) throws IOException, JSONException {

		String pathToSWN = "SentiWordNet_3.0.0_20130122.txt";
		SentiWordNet sentiwordnet = new SentiWordNet(pathToSWN);
		
		// Calculate scores for our good, bad, and recent movie tweets
		calculateDir(sentiwordnet, "good");
		calculateDir(sentiwordnet, "bad");
		calculateDir(sentiwordnet, "recent");
	}

	// Goes through all of the movies in a directory and prints out the SentiWordNet score of each movie
	public static void calculateDir(SentiWordNet sentiwordnet, String path)
			throws JSONException, IOException {
		File dir = new File(rootDir + path + "/tweets");
		File[] dirListing = dir.listFiles();
		if (dirListing != null) {
			for (File child : dirListing) {
				List<String> lines = Files.readAllLines(
						Paths.get(child.getAbsolutePath()),
						Charset.defaultCharset());
				String jsonText = lines.get(0);
				if (!jsonText.equals("None")) {
					JSONArray jsonarray = new JSONArray(jsonText);
					double totalScore = 0;
					int count = 0;
					// Go through each tweet of the movie
					for (int i = 0; i < jsonarray.length(); i++) {
						JSONObject obj = jsonarray.getJSONObject(i);

						String tweet = obj.getString("u'user_value'");
						// Calculate the SentiWordNet score
						double score = getTweetScore(tweet, sentiwordnet);
						// If a valid score is calculated, add it to the total
						if (score != -100) {
							totalScore += score;
							count += 1;
						}
					}

					DecimalFormat formatter = new DecimalFormat("#0.000");
					// Print out the movie and its corresponding SentiWordNet score
					System.out.println(getMovieTitle(child.getName()) + "," + formatter.format(totalScore/count));
				}

			}
		}

	}
	
	// Extract movie title from the JSON file name
	public static String getMovieTitle(String jsonString) {
		return jsonString.substring(0, jsonString.length() - 5).replace("_",
				" ");
	}

	// Given a tweet, find its SentiWordNet score by going through each word and finding the
	// average SentiWordNet score of all the words in the tweet
	public static double getTweetScore(String tweet, SentiWordNet sentiwordnet) {
		double totalScore = 0;
		int count = 0;
		String[] words = tweet.substring(2).split(" ");
		for (int i = 0; i < words.length; i++) {
			double wordScore = sentiwordnet.extract(words[i]);
			// Ignore if the word wasn't found in the dictionary
			if (wordScore != -100) {
				totalScore += wordScore;
				count += 1;
			}
		}

		// If no words were valid, return -100
		if (count == 0) {
			return -100;
		} else {
			// Return average score
			return totalScore / count;
		}
	}
}