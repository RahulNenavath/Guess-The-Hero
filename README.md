# Introduction:
### Title: Guess the Super Hero!
### Problem Statement:
Given a description of a `superhero`, return the superhero name <br>
### Example Input & Output:
Input description: `Knight of Dark, Gotham protector, Smart, Intelligent, martial artist, master of dark, educated` <br>
Output: `Batman`
### Dataset Description:
Dataset link: https://www.kaggle.com/datasets/jonathanbesomi/superheroes-nlp-dataset <br><br>
Total rows: 1450 <br>
Total columns: 81 <br>

### Solution:
The task is to map a given description to an entity name. <br> 
Challenges:
* `Limited number of records` for supervised machine learning approches. 
* There is `no target class`: Each record describes a unique super hero. Thereby not a regular classification & regression task
* Although `multiple superheros may have similar characteristics, each super hero is different`. Thereby not exactly clustering

Considering the input to the system, first and second points in challenges, I need to `construct superhero description` from the provided dataset. This transformation of structured information into unstructured text is `unconventional` but it is `efficient` this way. <br><br>
The assumption is this constructed superhero `description` will have `rich information` about the superhero. This description will help us match the input description to superhero name. <br><br>

`Solution`: Use `Semantic Search` to match the input description query to existing superhero descriptions and fetch top - k records. Later, use `Keyword Search` to find the records that have large number of similar words as of input description. <br><br>

### Tech Stack:
* Python - 3.8 <br>
* Spacy - 3.4 <br>
* Spacy Transformers - 1.1.8 <br>
* KeyBERT - 0.6.0 <br>
* hnswlib - 0.6.2 - Hierarchical Navigable Small World for Approximate Nearest Neightbour Search <br>
* Sentence Transformers - 2.2.2 <br>
* Text Distance - 4.5.0 <br>
* AWS  <br>
* Docker  <br>
* CI/CD  <br>