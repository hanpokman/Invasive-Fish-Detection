from src.neural_net import predict_species_from_length


class InvasiveDetector:
    def __init__(self, fish_db, model, stereo_vision=None, similarity_model=None):
        self.fish_db = fish_db
        self.model = model
        self.stereo = stereo_vision
        self.similarity_model = similarity_model
        self.last_result = None

    def detect(self, left_img, right_img):
        # measure length
        if self.stereo:
            fish_length = self.stereo.measure_fish_length(left_img, right_img)
        else:
            fish_length = 25.0

        # get candidates
        candidates = predict_species_from_length(self.model, fish_length, self.fish_db)

        # best match
        best_match = candidates[0]['species']
        best_score = candidates[0]['similarity']

        # check if invasive
        is_invasive = self.fish_db[best_match].get('invasive', False)

        result = {
            'species': best_match,
            'invasive': is_invasive,
            'length_cm': fish_length,
            'confidence': best_score,
            'top_candidates': candidates[:3]
        }

        self.last_result = result
        return result

    def get_last_result(self):
        return self.last_result