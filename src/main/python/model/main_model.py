class MainModel:
    def __init__(self):
        super(MainModel, self).__init__()

        # data
        self.__total_camera_used = None
        self.__camera_placement = None
        self.__properties_image = {}

        # image
        self.__list_original_image = []
        self.__list_undistorted_image = []
        self.__list_undistorted_drawing_image = []
        self.__list_original_undistorted_image = []
        self.__list_perspective_image = []
        self.__list_perspective_drawing_image = []
        self.__union_original_image = None
        self.__overlap_image = None
        self.__bird_view_image = None

        # video
        self.__list_frame_video = []
        self.__list_perspective_video = []
        self.__list_union_original_video = []
        self.__bird_view_video = None

    # ===================================== data=====================================
    @property
    def total_camera_used(self):
        return self.__total_camera_used

    @total_camera_used.setter
    def total_camera_used(self, value):
        self.__total_camera_used = value

    @property
    def camera_placement(self):
        return self.__camera_placement

    @camera_placement.setter
    def camera_placement(self, value):
        self.__camera_placement = value

    @property
    def properties_image(self):
        return self.__properties_image

    @properties_image.setter
    def properties_image(self, value):
        self.__properties_image = value

    # ===================================== image =====================================
    @property
    def list_original_image(self):
        return self.__list_original_image

    @list_original_image.setter
    def list_original_image(self, value):
        self.__list_original_image = value

    @property
    def list_undistorted_image(self):
        return self.__list_undistorted_image

    @list_undistorted_image.setter
    def list_undistorted_image(self, value):
        self.__list_undistorted_image = value

    @property
    def list_undistorted_drawing_image(self):
        return self.__list_undistorted_drawing_image

    @list_undistorted_drawing_image.setter
    def list_undistorted_drawing_image(self, value):
        self.__list_undistorted_drawing_image = value

    @property
    def list_original_undistorted_image(self):
        return self.__list_original_undistorted_image

    @list_original_undistorted_image.setter
    def list_original_undistorted_image(self, value):
        self.__list_original_undistorted_image = value

    @property
    def list_perspective_image(self):
        return self.__list_perspective_image

    @list_perspective_image.setter
    def list_perspective_image(self, value):
        self.__list_perspective_image = value

    @property
    def list_perspective_drawing_image(self):
        return self.__list_perspective_drawing_image

    @list_perspective_drawing_image.setter
    def list_perspective_drawing_image(self, value):
        self.__list_perspective_drawing_image = value

    @property
    def union_original_image(self):
        return self.__union_original_image

    @union_original_image.setter
    def union_original_image(self, value):
        self.__union_original_image = value

    @property
    def overlap_image(self):
        return self.__overlap_image

    @overlap_image.setter
    def overlap_image(self, value):
        self.__overlap_image = value

    @property
    def bird_view_image(self):
        return self.__bird_view_image

    @bird_view_image.setter
    def bird_view_image(self, value):
        self.__bird_view_image = value

    # ===================================== video =====================================
    @property
    def list_frame_video(self):
        return self.__list_frame_video

    @list_frame_video.setter
    def list_frame_video(self, value):
        self.__list_frame_video = value

    @property
    def list_perspective_video(self):
        return self.__list_perspective_video

    @list_perspective_video.setter
    def list_perspective_video(self, value):
        self.__list_perspective_video = value

    @property
    def list_union_original_video(self):
        return self.__list_union_original_video

    @list_union_original_video.setter
    def list_union_original_video(self, value):
        self.__list_union_original_video = value

    @property
    def bird_view_video(self):
        return self.__bird_view_video

    @bird_view_video.setter
    def bird_view_video(self, value):
        self.__bird_view_video = value
