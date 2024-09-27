
class SpellCorrection:
    def __init__(self,nlp,model) :
        self.nlp = nlp
        self.model = model
        self.num_words=10

    def damerau_levenshtein_distance(self,s1, s2):
        """
        Calculate the Damerau-Levenshtein distance between two strings.
        
        Args:
            s1 (str): The first string. The correct words
            s2 (str): The second string. The wrong words
            
        Returns:
            int: The Damerau-Levenshtein distance.
        """
        # Create a matrix to hold the distances
        len_s1, len_s2 = len(s1), len(s2)
        distance_matrix = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

        # Initialize the matrix with incremental distances
        for i in range(len_s1 + 1):
            distance_matrix[i][0] = i
        for j in range(len_s2 + 1):
            distance_matrix[0][j] = j

        # Fill the matrix with distances
        for i in range(1, len_s1 + 1):
            for j in range(1, len_s2 + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1

                # Minimum of deletion, insertion, and substitution
                distance_matrix[i][j] = min(
                    distance_matrix[i - 1][j] + 1,         # Deletion
                    distance_matrix[i][j - 1] + 1,         # Insertion
                    distance_matrix[i - 1][j - 1] + cost   # Substitution
                )

                # Check for transposition
                if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                    distance_matrix[i][j] = min(
                        distance_matrix[i][j],
                        distance_matrix[i - 2][j - 2] + cost  # Transposition
                    )

        # The final distance is in the bottom-right cell of the matrix
        return distance_matrix[len_s1][len_s2]



    def detect_spell_error(self,sentences):
        # Non word error detection
        wrong_words = []
        words_pos = []    
        temp_sent = []
        
        for token in self.nlp(sentences.lower()):
            if token.text != " ":
                temp_sent.append(str(token))
        
        
        output = list(self.model.vocab.lookup(temp_sent))
        for i,w in enumerate(output):
            if w == '<UNK>' and temp_sent[i].isalpha():
                wrong_words.append((temp_sent[i-1],temp_sent[i]))
                words_pos.append(i)

        return wrong_words,words_pos
    
    def detect_real_error(self,sentences):
        #https://aclanthology.org/O13-1022.pdf
        wrong_words = []
        words_pos = []    
        temp_sent = []

        for token in self.nlp(sentences.lower()):
            if token.text != " " and token.text.isalpha():       
                temp_sent.append(str(token))

        i = 0
        while i < len(temp_sent) - 1:
            bigram = (temp_sent[i], temp_sent[i + 1])   
            
            # Get the probability of the bigram
            probability = self.model.score(bigram[1], [bigram[0]])
            
            if probability < 0.001:
                # Add the bigram to the list of wrong words
                wrong_words.append(bigram)
                words_pos.append((i, i+1))
                
                # Skip the next word by incrementing i by 2
                i += 2
            else:
                # Increment i by 1 if no error detected
                i += 1
        
        return wrong_words,words_pos  
    
    def preproc_sent(self,sentences):
        temp_sent =[]
        
        for token in self.nlp(sentences):
            if token.text != " ":
                temp_sent.append(str(token))

        return temp_sent
    
    def possible_words(self,wrd_lst,wrong_word):
        pos_words = {}
        sor_out = {}
        lower_bound = int(len(wrong_word[1])*0.8)
        upper_bound = int(len(wrong_word[1])*1.2)
        
        all_words=[key for key, value in wrd_lst.items() if value >= lower_bound and value <= upper_bound]
        
        for word in all_words:
            score = self.damerau_levenshtein_distance(word,wrong_word[1])
            pos_words[word]=score
        sorted_keys = sorted(pos_words, key=pos_words.get, reverse=False)[:self.num_words]
        
        for pob_word in sorted_keys:
            prob = self.model.score(pob_word, [wrong_word[0]])
            sor_out[pob_word] = prob        
        sorted_keys = sorted(sor_out, key=sor_out.get, reverse=True)
            
        return sorted_keys    
   
