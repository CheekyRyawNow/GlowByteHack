import gc

class GarbageService:
    # Doesn't work because of variable reference
    @staticmethod
    def delete_variables(*variables):
        for variable in variables:
            del variable
        gc.collect()