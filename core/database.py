class BaseRepository:
    @staticmethod
    def save_model(instance):
        instance.save()
        return instance