# Ethan Chang
# echang28@u.rochester.edu
# created/tested using SageMath-10-4
import numpy as np

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
            # Extract the tone from the  character of the syllable
            tone = int(syllable[-1])
            tones.append(tone)
          except (IndexError, ValueError):
            print(f"Skipping invalid syllable: {syllable}")
  return tones

# Files
df_tones = extract_tones('/Users/ethanchang/Downloads/df.txt')
zsz_tones = extract_tones('/Users/ethanchang/Downloads/zsz.txt')
test_tones = extract_tones('/Users/ethanchang/Downloads/zsz-test.txt')
test_tones2 = extract_tones('/Users/ethanchang/Downloads/df-test.txt')

def construct_mm(tones):
  '''
  Function that constructs the Markov matrix for the 4 tones
  '''
  # Initialize a 4x4 (for the five tones) matrix with zeros 
  matrix = Matrix(RR, 4, 4, lambda i, j: 0)
    
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
test2_mm = construct_mm(test_tones2)

def equil_vec(transition_matrix, tol=1e-10, max_iter=100000):
  '''
  Function that identifies the equilibrium vector through continuous applications of Markov matrix
  '''
  # Initialize random 1 x 4 vector with 1/4 as starting values
  steady_state = np.ones(4) / 4 
  # Applies Markov matrix to the initialized vector for the number of iterations (or until it hits tolerance for change)
  for i in range(max_iter):
    new_steady_state = steady_state @ transition_matrix
    if np.allclose(new_steady_state, steady_state, atol=tol):
      break
    steady_state = new_steady_state
    return steady_state
  
# Find the equilibrium vectors for each matrix
df_equil = equil_vec(df_mm)
zsz_equil = equil_vec(zsz_mm)
test_equil = equil_vec(test_mm)
test2_equil = equil_vec(test2_mm)

def euc_dist(vec1, vec2):
  '''
  Function to compute the Euclidean distance between two vectors
  '''
  return sqrt(sum((vec1[i] - vec2[i])^2 for i in range(len(vec1))))

def predict_author(file_path):
  '''
  Function that takes the path of a text file and predicts the author
  '''
  # Extract tones from the user input file
  tones = extract_tones(file_path)
    
  # Construct the Markov matrix for the input tones
  mm = construct_mm(tones)
    
  # Find the equilibrium vector for the input Markov matrix
  equil = equil_vec(mm)
    
  # Compute Euclidean distances to reference equilibrium vectors
  df_dist = euc_dist(equil, df_equil)
  zsz_dist = euc_dist(equil, zsz_equil)
    
  # Determine which author the input text is closer to
  if df_dist < zsz_dist:
      predicted_author = "Du Fu"
  elif df_dist == zsz_dist:
      predicted_author = "Unable to differentiate"
  else:
      predicted_author = "Zhu Shuzhen"
    
  # Output the prediction
  print(f"Predicted author: {predicted_author}")
  print(f"Distance to Du Fu: {df_dist}, Distance to Zhu Shuzhen: {zsz_dist}")
    
  return

# User usage
file_path = input("Enter the path to the text file: ")
predict_author(file_path)



# Code for other attempts, testing, and/or methods
'''
# Attempt to use iteration method with SageMath functions
def equil_vec(mm, tol=1e-10, max_iter=100000):
  Function to find the equilibrium vector using SageMath
  Applies the Markov matrix repeatedly to an initial vector until convergence.

  # Initialize the vector uniformly (equivalent to the new code)
  x = vector(RR, [1/4, 1/4, 1/4, 1/4])  # Uniform initial vector for the 4-tone system
    
  for _ in range(max_iter):
      x_new = mm * x  # Matrix-vector multiplication
      # Check if the difference between the new and old vectors is below tolerance
      if max(abs(x_new[i] - x[i]) for i in range(4)) < tol:
        return x_new / sum(x_new)  # Normalize to ensure it sums to 1
      x = x_new
    
  raise ValueError("Equilibrium vector did not converge within the specified iterations")


# Find the equilibrium vectors for each matrix
df_equil = equil_vec(df_mm)
zsz_equil = equil_vec(zsz_mm)
test_equil = equil_vec(test_mm)
test2_equil = equil_vec(test_mm)

print(f"Equilibrium vector for df: {df_equil}")
print(f"Equilibrium vector for zsz: {zsz_equil}")
print(f"Equilibrium vector for the test set: {test_equil}")
print(f"Equilibrium vector for the test set2: {test2_equil}")

# attempted to find equilibrium vec by using eigenvectors found using SageMath's function
def equil_vec(mm):
  Function that creates the equilibrium vector from the Markov matrix

  eigen_data = mm.eigenvectors_right()

  # Find the eigenvector corresponding to eigenvalue 1
  for eigenvalue, eigenvectors, _ in eigen_data:
    if eigenvalue == 1:
      steady_state = eigenvectors[0]  # Pick the first eigenvector corresponding to 1
      steady_state = steady_state / sum(steady_state)  # Normalize to sum to 1
      return steady_state

  raise ValueError("No equilibrium vector found")

print(f"Equilibrium vector for df: {df_equil}")
print(f"Equilibrium vector for zsz: {zsz_equil}")
print(f"Equilibrium vector for the test set: {test_equil}")
print(f"The predicted author based on equilibrium vectors is: {predicted_author}")

# attempt to use Frobenius norm to find distance between matrices
def frobenius_norm(A, B):
  return sqrt(sum((A[i,j] - B[i,j])^2 for i in range(A.nrows()) for j in range(A.ncols())))

# Compare the matrices
df_zsz_norm = frobenius_norm(df_mm, zsz_mm)
df_test_norm = frobenius_norm(df_mm, test_mm)
zsz_test_norm = frobenius_norm(zsz_mm, test_mm)
df_test2_norm = frobenius_norm(df_mm, test2_mm)
zsz_test2_norm = frobenius_norm(zsz_mm, test2_mm)

print(f"Frobenius norm between df and zsz: {df_zsz_norm}")
print(f"Frobenius norm between df and test: {df_test_norm}")
print(f"Frobenius norm between zsz and test: {zsz_test_norm}")
print(f"Frobenius norm between df and test2: {df_test2_norm}")
print(f"Frobenius norm between zsz and test2: {zsz_test2_norm}")

'''
