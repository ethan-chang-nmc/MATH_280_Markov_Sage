# Ethan Chang
# echang28@u.rochester.edu
# created/tested using SageMath-10-4

def extract_tones(file_path):
  '''
  Function to extract each tone within the files
  '''
  tones = []
  with open(file_path, 'r') as file:
      for line in file:
          syllables = line.strip().split()
          for syllable in syllables:
              if syllable:
                  try:
                      # Extract the tone from the last character of the syllable
                      tone = int(syllable[-1])
                      tones.append(tone)
                  except (IndexError, ValueError):
                      print(f"Skipping invalid syllable: {syllable}")
  return tones

# Files
df_tones = extract_tones('/Users/ethanchang/Downloads/df.txt')
zsz_tones = extract_tones('/Users/ethanchang/Downloads/zsz.txt')
test_tones = extract_tones('/Users/ethanchang/Downloads/zsz-test.txt')


def construct_mm(tones):
  '''
  Function that constructs the Markov matrix for the 4 tones
  '''
  # Initialize a 4x4 (for the five tones) matrix with zeros 
  matrix = Matrix(QQ, 4, 4, lambda i, j: 0)
    
  # Count the transitions
  for i in range(len(tones) - 1):
      current_tone = tones[i] - 1
      next_tone = tones[i + 1] - 1
      matrix[current_tone, next_tone] += 1
    
  # Normalize the rows to convert to probabilities
  for i in range(4):
      row_sum = sum(matrix[i])
      if row_sum > 0:
          matrix[i] = [matrix[i][j] / row_sum for j in range(4)]
    
  return matrix

# Construct the matrices
df_mm = construct_mm(df_tones)
zsz_mm = construct_mm(zsz_tones)
test_mm = construct_mm(test_tones)

# Print the Markov matrices
print("Markov Matrix for df:")
print(df_mm)
print("Markov Matrix for zsz:")
print(zsz_mm)
print("Markov Matrix for the test set:")
print(test_mm)

def equil_vec(mm):
    '''
    Function that creates the equilibrium vector from the Markov matrix
    '''
    eigen_data = mm.eigenvectors_right()

    # Find the eigenvector corresponding to eigenvalue 1
    for eigenvalue, eigenvectors, _ in eigen_data:
        if eigenvalue == 1:
            steady_state = eigenvectors[0]  # Pick the first eigenvector corresponding to 1
            print(f"Raw Eigenvector before normalization: {steady_state}")  # Debugging line
            steady_state = steady_state / sum(steady_state)  # Normalize to sum to 1
            return steady_state

    raise ValueError("No equilibrium vector found")


# Find the equilibrium vectors for each matrix
df_equil = equil_vec(df_mm)
zsz_equil = equil_vec(zsz_mm)
test_equil = equil_vec(test_mm)

def euc_dist(vec1, vec2):
    '''
    Function to compute the Euclidean distance between two vectors
    '''
    return sqrt(sum((vec1[i] - vec2[i])^2 for i in range(len(vec1))))

# Compute the distances between test set and training
df_dist = euc_dist(df_equil, test_equil)
zsz_dist = euc_dist(zsz_equil, test_equil)

# Determine which author the test set is closer to
if df_dist < zsz_dist:
    predicted_author = "Tu Fu"
elif df_dist == zsz_dist:
    predicted_author = "Unable to differentiate"
else:
    predicted_author = "Zhu Shuzhen"

print(f"Equilibrium vector for df: {df_equil}")
print(f"Equilibrium vector for zsz: {zsz_equil}")
print(f"Equilibrium vector for the test set: {test_equil}")
print(f"The predicted author based on equilibrium vectors is: {predicted_author}")
