import gc

class GarbageService:
    @staticmethod
    def delete_variables(*variables):
        for variable in variables:
            del variable
        gc.collect()