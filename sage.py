#Ethan Chang
#echang28@u.rochester.edu

def extract_tones(file_path):
  '''
  function to extract each tone within the files
  '''
  tones = []
  with open(file_path, 'r') as file:
      for line in file:
          syllables = line.strip().split(',')
          for syllable in syllables:
              # Extract the tone
              tone = int(syllable[-1])
              tones.append(tone)
  return tone

#files
df_tones = extract_tones('C:\Users\etcha\Downloads\MATH 280\zsz.txt')
zsz_tones = extract_tones('C:\Users\etcha\Downloads\MATH 280\df.txt')


def construct_markov_matrix(tones):
  '''
  function that constructs the Markov matrix for the 5 tones
  '''
  # Initialize a 5x5 (for the five tones) matrix with zeros 
  matrix = Matrix(QQ, 5, 5, lambda i, j: 0)
    
  # Count the transitions
  for i in range(len(tones) - 1):
      current_tone = tones[i] - 1
      next_tone = tones[i + 1] - 1
      matrix[current_tone, next_tone] += 1
    
  # Normalize the rows to convert to probabilities
  for i in range(5):
      row_sum = sum(matrix[i])
      if row_sum > 0:
          matrix[i] = [matrix[i][j] / row_sum for j in range(5)]
    
  return matrix
