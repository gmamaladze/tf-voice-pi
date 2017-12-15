import abc

NOT_SET = -1


class Warrantor(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def is_confident(self, index, score):
        pass

    @abc.abstractmethod
    def reset(self):
        pass


class NullWarrantor(Warrantor):
    def is_confident(self, index, score):
        return True

    def reset(self):
        pass


class SimpleWarrantor(Warrantor):

    def __init__(self, score):
        Warrantor.__init__(self)
        self.score = score

    def is_confident(self, index, score):
        return score > self.score

    def reset(self):
        pass


class HitCountWarrantor(Warrantor):

    def __init__(self, hit_scores=None):
        Warrantor.__init__(self)
        if hit_scores is None:
            hit_scores = [.9, .6, .3]
        self.last_idx = NOT_SET
        self.avg_score = 0
        self.hit_count = 0
        self.hit_scores = hit_scores

    def is_confident(self, index, score):
        if self.last_idx == NOT_SET:
            self.last_idx = index
            self.avg_score = score
        if self.last_idx != index:
            self.reset()
        else:
            self.hit_count += 1
            self.avg_score = (self.avg_score + score) / 2
        if self.hit_count == 0:
            return False
        hit_score_index = min(self.hit_count, len(self.hit_scores)) - 1
        threshold_score = self.hit_scores[hit_score_index]
        return self.avg_score > threshold_score

    def reset(self):
        self.last_idx = NOT_SET
        self.avg_score = 0
        self.hit_count = 0
