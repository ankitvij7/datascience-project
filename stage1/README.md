# UW-Madison CS 839 Data Science

## Team Koala Ninja (10)
* Ankit Vij
* Amanpreet Singh Saini
* Joel Haynie

## Project Stage 1
Entity type: "People Names"; Tag in file with(as in assignment):  **<person>...</>**

Prefix Titles are not included:**Dr., Mr., Mrs., Ms., CEO, President, etc**

Suffix Titles are not included: **PHD, OBE, CPA, PE, etc**

Suffix Names are included: **Sr., Jr., the third, III, IV, etc**

First or Last Names only are considered a Person.

Names when used in organizations/schools/campaigns are persons eg **Godman Sachs, Trump campaign**

All files should be in ASCII and English

File Name: **SOURCE-DATE-FIRST_WORD_IN_TITLE.txt, ex "CNN-02-16-2018-flu.txt"**

Names with Ownership: Do not include the **'s**, eg **<person>Joel Haynie</>'s face**

Names when used in proper nouns are not persons eg **Guillain-Barré syndrome**

Fictional Characters are persons eg **Harry Potter, Mona Lisa, Venus** (this one we should debate)

# Text for Paper:
* the names of all team members.
* Class: CS 839 - Data Science Spring 2018
  * Prof: Dr. Anhai Doan
  * Date: 02/28/2018
  * RE: Project Stage 1
  * Team Koala Ninja (10)
  * Ankit Vij
  * Amanpreet Singh Saini
  * Joel Haynie

* the entity type that you have decided to extract, give a few examples of mentions of this entity type. 
  * Entity type: "People Names"
  * Examples: <person>Donald Trump</>; <person>Trump</> <person>Donald Trump Jr.</>

* The total number of mentions that you have marked up is:
  * We have marked up 1561 mentions

* the number of documents in set I, the number of mentions in set I.
  * The Training Set (i) is made up of 54 Files with 956 Mentions.
* the number of documents in set J, the number of mentions in set J.
  * The Test Set (j) is made up of 26 Files with 605 Mentions.
* the type of the classifier that you selected after performing cross validation on set I *the first time*, and the precision, recall, F1 of this classifier (on set I). This classifier is referred to as classifier M in the description above. 
  * We FIRST chose the ___________  Classifier because it had the best Precision, Recall & F1 given below:
* the type of the classifier that you have finally settled on *before* the rule-based postprocessing step, and the precision, recall, F1 of this classifier (on set J). This classifier is referred to as classifier X in the description above. 
  * We eventually chose the ___________ Classifier because it had the best precision, Recall & F1 after we were able to tweak it, as seen below:
* if you have done any rule-based post-processing, then give examples of rules that you have used, and describe where can we find all the rules (e.g., is it in the code directory somewhere?). 
  * We did the following rule-based Post-processing: 
* Report the precision, recall, F1 of classifier Y (see description above) on set J. This is the final classifier (plus rule-based post-processing if you have done any). 
  * Here is our final precision, recall and F1 from the ___________ Classifier: 
* If you have not reached precision of at least 90% and recall of at least 60%, provide a discussion on why, and what else can you possibly do to improve the accuracy. 
  * We think to improve accuracy we could increase our training set thus helping us to not over fit to our training set I.
* Provide any other information that you would like. 
  * Thoughts?