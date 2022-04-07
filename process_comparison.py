def conceptual_similarity(nGc, nG1, nG2):
    return (2*nGc)/(nG1 + nG2)


def relational_similarity(mGc, mGcG1, mGcG2):
    return (2*mGc)/(mGcG1 + mGcG2)


def calculate_a(nGc, mGcG1, mGcG2):
    return (2*nGc)/(2*nGc+mGcG1 + mGcG2)