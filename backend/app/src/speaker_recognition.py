import numpy as np
from sklearn.cluster import OPTICS

def speaker_recognition(embeddings):
    if len(embeddings) > 2:
        clustering = OPTICS(min_samples=2).fit(np.array(embeddings))
    else:
        clustering = None
    
    return clustering