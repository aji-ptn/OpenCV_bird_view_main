import numpy as np

from .additional_function import read_image
import cv2
from .merge_original_image import merge_original_image
from .video_controller import VideoController
import yaml
from subprocess import call


class MainController:
    def __init__(self, appctx, model):
        """

        Args:
            model:
        """
        super(MainController, self).__init__()
        self.app_ctxt = appctx
        self.model = model
        self.video_controller = VideoController(self.app_ctxt, self)

        # self.matrix_k = []
        # self.coefficient = []
        # self.dimension = []
        # self.data_config = None

    def initial_properties(self):
        # self.matrix_k = []
        # self.coefficient = []
        # self.dimension = []
        if self.model.data_config is None:
            self.model.properties_image = {}
        cam_total = self.model.total_camera_used
        self.model.calibration_image = {"matrix_k": [], "new_matrix_k": [], "dis_coefficient": [], "dimension": []}
        self.model.list_original_image = []
        self.model.list_original_undistorted_image = [None] * cam_total
        self.model.list_undistorted_image = [None] * cam_total
        self.model.list_undistorted_drawing_image = [None] * cam_total
        self.model.list_perspective_image = [None] * cam_total
        self.model.list_perspective_drawing_image = [None] * cam_total

    def list_image_data(self, path_image, i):
        print(path_image)
        self.model.list_original_image.append(read_image(path_image))
        self.process_original_undistorted(i)

    def list_intrinsic_data(self, path_parameter):
        K, D, dimension = self.read_parameter(path_parameter)
        print(K, D, list(dimension))
        print(self.model.data_config)
        print(self.model.calibration_image)
        # print(self.model.calibration_image["matrix_k"])
        self.model.calibration_image["matrix_k"].append(K)
        self.model.calibration_image["dis_coefficient"].append(D)
        self.model.calibration_image["dimension"].append(dimension)
        print("==============================")
        print(self.model.calibration_image["dimension"])
        print("==============================")

    def update_union_original_image(self):
        self.model.union_original_image = merge_original_image(self.model.list_original_image)

    def update_intrinsic_parameter(self, i):
        keys = list(self.model.properties_image)
        self.model.properties_image[keys[i]]["Ins"]["Fx"] = float(self.model.calibration_image["matrix_k"][i][0][0])
        self.model.properties_image[keys[i]]["Ins"]["Fy"] = float(self.model.calibration_image["matrix_k"][i][1][1])
        self.model.properties_image[keys[i]]["Ins"]["Icx"] = float(self.model.calibration_image["matrix_k"][i][0][2])
        self.model.properties_image[keys[i]]["Ins"]["Icy"] = float(self.model.calibration_image["matrix_k"][i][1][2])
        self.model.properties_image[keys[i]]["Ins"]["Width"] = int(self.model.calibration_image["dimension"][i][0])
        self.model.properties_image[keys[i]]["Ins"]["Height"] = int(self.model.calibration_image["dimension"][i][1])

    def process_undistorted_image(self, i):
        keys = list(self.model.properties_image)
        new_matrix = self.model.calibration_image["matrix_k"][i].copy()
        new_matrix[0, 0] = self.model.properties_image[keys[i]]["Ins"]["Fx"]
        new_matrix[1, 1] = self.model.properties_image[keys[i]]["Ins"]["Fy"]
        new_matrix[0, 2] = self.model.properties_image[keys[i]]["Ins"]["Icx"]
        new_matrix[1, 2] = self.model.properties_image[keys[i]]["Ins"]["Icy"]

        self.model.calibration_image["new_matrix_k"] = new_matrix

        width = self.model.properties_image[keys[i]]["Ins"]["Width"]
        height = self.model.properties_image[keys[i]]["Ins"]["Height"]
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.model.calibration_image["matrix_k"][i],
                                                         self.model.calibration_image["dis_coefficient"][i], np.eye(3),
                                                         self.model.calibration_image["new_matrix_k"],
                                                         (width, height), cv2.CV_16SC2)

        path_map_x_anypoint = self.app_ctxt.get_resource("data_config/maps/map_x_" + str(i) + ".npy")
        path_map_y_anypoint = self.app_ctxt.get_resource("data_config/maps/map_y_" + str(i) + ".npy")

        np.save(path_map_x_anypoint, map1)
        np.save(path_map_y_anypoint, map2)

        undistorted = cv2.remap(self.model.list_original_image[i], map1, map2,
                                interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        self.model.list_undistorted_image[i] = undistorted
        self.draw_point_position("src", keys, i)

    def process_original_undistorted(self, i):
        width, height = self.model.calibration_image["dimension"][i]
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.model.calibration_image["matrix_k"][i],
                                                         self.model.calibration_image["dis_coefficient"][i], np.eye(3),
                                                         self.model.calibration_image["matrix_k"][i],
                                                         (int(width), int(height)),
                                                         cv2.CV_16SC2)
        self.model.list_original_undistorted_image[i] = cv2.remap(self.model.list_original_image[i], map1, map2,
                                                                  interpolation=cv2.INTER_LINEAR,
                                                                  borderMode=cv2.BORDER_CONSTANT)

    def load_config(self, config_file):
        with open(config_file, "r") as file:
            data_config = yaml.safe_load(file)
        self.model.data_config = True
        self.model.properties_image = data_config

    def save_config_to_file(self, data):
        print("save")
        properties_image = self.model.properties_image
        # properties_image["camera_used"] = self.model.total_camera_used
        # properties_image["camera_placement"] = self.model.camera_placement
        print(properties_image)
        with open(data, "w") as outfile:
            yaml.dump(properties_image, outfile, default_flow_style=False)

    def process_perspective_image(self, i):
        print("process perspective image")
        keys = list(self.model.properties_image)
        canvas = self.model.properties_image[keys[i]]["dst"]["Width"], self.model.properties_image[keys[i]]["dst"][
            "Height"]
        src = np.float32(
            [[self.model.properties_image[keys[i]]["src"]["point1_x"],
              self.model.properties_image[keys[i]]["src"]["point1_y"]],
             [self.model.properties_image[keys[i]]["src"]["point2_x"],
              self.model.properties_image[keys[i]]["src"]["point2_y"]],
             [self.model.properties_image[keys[i]]["src"]["point3_x"],
              self.model.properties_image[keys[i]]["src"]["point3_y"]],
             [self.model.properties_image[keys[i]]["src"]["point4_x"],
              self.model.properties_image[keys[i]]["src"]["point4_y"]]])
        dst = np.float32(
            [[self.model.properties_image[keys[i]]["dst"]["point1_x"],
              self.model.properties_image[keys[i]]["dst"]["point1_y"]],
             [self.model.properties_image[keys[i]]["dst"]["point2_x"],
              self.model.properties_image[keys[i]]["dst"]["point2_y"]],
             [self.model.properties_image[keys[i]]["dst"]["point3_x"],
              self.model.properties_image[keys[i]]["dst"]["point3_y"]],
             [self.model.properties_image[keys[i]]["dst"]["point4_x"],
              self.model.properties_image[keys[i]]["dst"]["point4_y"]]])

        matrix = cv2.getPerspectiveTransform(src, dst)
        self.model.list_perspective_image[i] = cv2.warpPerspective(self.model.list_undistorted_image[i], matrix, canvas)
        self.draw_point_position("dst", keys, i)

    def draw_point_position(self, position, keys, i):
        font = cv2.FONT_HERSHEY_SIMPLEX
        if position == "dst":
            self.model.list_perspective_drawing_image[i] = self.model.list_perspective_image[i].copy()
            image = self.model.list_perspective_drawing_image[i]
            font_color = (77, 180, 215)
        elif position == "src":
            self.model.list_undistorted_drawing_image[i] = self.model.list_undistorted_image[i].copy()
            image = self.model.list_undistorted_drawing_image[i]
            font_color = (72, 191, 145)
        else:
            image = None
            font_color = None
        cv2.circle(image, (self.model.properties_image[keys[i]][position]["point1_x"],
                           self.model.properties_image[keys[i]][position]["point1_y"]), 20, (0, 0, 255), 5)
        cv2.putText(image, '1', (self.model.properties_image[keys[i]][position]["point1_x"],
                                 self.model.properties_image[keys[i]][position]["point1_y"]), font,
                    5, font_color, 5, cv2.LINE_AA)
        cv2.circle(image, (self.model.properties_image[keys[i]][position]["point2_x"],
                           self.model.properties_image[keys[i]][position]["point2_y"]), 20, (0, 0, 255), 5)
        cv2.putText(image, '2', (self.model.properties_image[keys[i]][position]["point2_x"],
                                 self.model.properties_image[keys[i]][position]["point2_y"]), font,
                    5, font_color, 5, cv2.LINE_AA)
        cv2.circle(image, (self.model.properties_image[keys[i]][position]["point3_x"],
                           self.model.properties_image[keys[i]][position]["point3_y"]), 20, (0, 0, 255), 5)
        cv2.putText(image, '3', (self.model.properties_image[keys[i]][position]["point3_x"],
                                 self.model.properties_image[keys[i]][position]["point3_y"]), font,
                    5, font_color, 5, cv2.LINE_AA)
        cv2.circle(image, (self.model.properties_image[keys[i]][position]["point4_x"],
                           self.model.properties_image[keys[i]][position]["point4_y"]), 20, (0, 0, 255), 5)
        cv2.putText(image, '4', (self.model.properties_image[keys[i]][position]["point4_x"],
                                 self.model.properties_image[keys[i]][position]["point4_y"]), font,
                    5, font_color, 5, cv2.LINE_AA)
        if position == "dst":
            self.model.list_perspective_drawing_image[i] = image
        elif position == "src":
            self.model.list_undistorted_drawing_image[i] = image

    @classmethod
    def read_parameter(cls, path_parameter):
        file = cv2.FileStorage(path_parameter, cv2.FILE_STORAGE_READ)
        camera_matrix = file.getNode("camera_matrix").mat()
        dist_coefficient = file.getNode("dist_coeffs").mat()
        resolution = file.getNode("resolution").mat().flatten()
        file.release()
        K = np.array(camera_matrix)
        D = np.array(dist_coefficient)
        dimension = np.array(resolution)

        return K, D, dimension

    def process_bird_view(self, activation, image_sources):
        if image_sources == "image":
            image = self.model.list_perspective_image
        else:
            image = self.model.list_perspective_video
        print("Bird view")
        image = [image[0],
                 cv2.rotate(image[1], cv2.ROTATE_90_COUNTERCLOCKWISE),
                 cv2.rotate(image[2], cv2.ROTATE_90_CLOCKWISE),
                 cv2.rotate(image[3], cv2.ROTATE_180)]

        if image[3].shape[1] == image[0].shape[1] and image[2].shape[0] == image[1].shape[0]:
            canvas_bird_view = np.zeros([image[1].shape[0], image[0].shape[1], 3], dtype=np.uint8)
            right_limit = canvas_bird_view.shape[1] - image[2].shape[1]
            rear_limit = canvas_bird_view.shape[0] - image[3].shape[0]

            # image[0] = self.remove_black(image[0])
            # image[1] = self.remove_black(image[1])
            # image[2] = self.remove_black(image[2])
            # image[3] = self.remove_black(image[3])

            canvas_bird_view[0:0 + image[1].shape[0], 0:0 + image[1].shape[1]] = image[1]
            canvas_bird_view[0:0 + image[2].shape[0], right_limit:right_limit + image[2].shape[1]] = image[2]
            canvas_bird_view[0:0 + image[0].shape[0], 0:0 + image[0].shape[1]] = image[0]
            canvas_bird_view[rear_limit:rear_limit + image[3].shape[0], 0:0 + image[3].shape[1]] = image[3]
            # self.model.overlap_image = canvas_bird_view

            if activation == "overlap":
                list_overlapping = self.transparency_bird_view(image, right_limit, rear_limit)
                canvas_bird_view[0:0 + list_overlapping[0].shape[0], 0:0 + list_overlapping[0].shape[1]] = \
                list_overlapping[0]  # front left
                canvas_bird_view[rear_limit:rear_limit + list_overlapping[2].shape[0],
                0:0 + list_overlapping[2].shape[1]] = list_overlapping[2]  # left rear
                canvas_bird_view[0:0 + list_overlapping[1].shape[0],
                right_limit:right_limit + list_overlapping[1].shape[1]] = list_overlapping[1]  # front right
                canvas_bird_view[rear_limit:rear_limit + list_overlapping[3].shape[0],
                image[3].shape[1] - image[2].shape[1]
                : image[3].shape[1] - image[2].shape[1] +
                  list_overlapping[3].shape[1]] = list_overlapping[3]  # right rear
                # self.model.overlap_image = canvas_bird_view

            else:
                canvas_bird_view = self.bird_view_combine_overlapping(image)
                canvas_bird_view = cv2.cvtColor(canvas_bird_view, cv2.COLOR_BGRA2BGR)
                # self.model.overlap_image = canvas_bird_view

            return canvas_bird_view

    @classmethod
    def transfer(cls, src):
        # src = cv2.resize(src, (int(src.shape[1]/2), int(src.shape[0]/2)))
        tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(src)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)
        # cv2.imwrite("image.jpg", dst)
        return dst

    def bird_view_combine_overlapping(self, image):
        # cv2.imwrite("image1.jpg", image[3])
        for i in range(len(image)):
            image[i] = self.transfer(image[i])

        final_image_front = np.zeros([image[1].shape[0], image[0].shape[1], 4], dtype=np.uint8)
        final_image_left = np.zeros([image[1].shape[0], image[0].shape[1], 4], dtype=np.uint8)
        final_image_right = np.zeros([image[1].shape[0], image[0].shape[1], 4], dtype=np.uint8)
        final_image_rear = np.zeros([image[1].shape[0], image[0].shape[1], 4], dtype=np.uint8)

        right_limit = final_image_right.shape[1] - image[2].shape[1]
        rear_limit = final_image_rear.shape[0] - image[3].shape[0]

        final_image_left[0:0 + image[1].shape[0], 0:0 + image[1].shape[1]] = image[1]
        final_image_right[0:0 + image[2].shape[0], right_limit:right_limit + image[2].shape[1]] = image[2]
        final_image_front[0:0 + image[0].shape[0], 0:0 + image[0].shape[1]] = image[0]
        final_image_rear[rear_limit:rear_limit + image[3].shape[0], 0:0 + image[3].shape[1]] = image[3]

        res = final_image_left[:]
        cnd = final_image_right[:, :, 3] > 0
        res[cnd] = final_image_right[cnd]
        cnd = final_image_front[:, :, 3] > 0
        res[cnd] = final_image_front[cnd]
        cnd = final_image_rear[:, :, 3] > 0
        res[cnd] = final_image_rear[cnd]

        return res

    @classmethod
    def transparency_bird_view(cls, image, right_limit, rear_limit):
        print(image)
        print(len(image))
        image_overlap = [None] * len(image)
        crop_front_left = image[0][0:image[0].shape[0], 0:image[1].shape[1]]
        crop_left_front = image[1][0:image[0].shape[0], 0:image[1].shape[1]]
        image_overlap[0] = cv2.addWeighted(crop_front_left, 0.5, crop_left_front, 0.5, 0)  # overlap_front_left

        crop_front_right = image[0][0:image[0].shape[0], right_limit:right_limit + image[2].shape[1]]
        crop_right_front = image[2][0:image[0].shape[0], 0:image[2].shape[1]]
        image_overlap[1] = cv2.addWeighted(crop_front_right, 0.5, crop_right_front, 0.5, 0)  # overlap_front_right

        crop_left_rear = image[1][rear_limit:rear_limit + image[3].shape[0], 0:image[1].shape[1]]
        crop_rear_left = image[3][0:image[3].shape[0], 0:image[1].shape[1]]
        image_overlap[2] = cv2.addWeighted(crop_left_rear, 0.5, crop_rear_left, 0.5, 0)  # overlap_left_rear

        crop_right_rear = image[2][rear_limit:rear_limit + image[3].shape[0], 0:image[2].shape[1]]
        crop_rear_right = image[3][0:image[3].shape[0], image[3].shape[1] - image[2].shape[1]:
                                                        image[3].shape[1] - image[2].shape[1] + image[3].shape[1]]
        image_overlap[3] = cv2.addWeighted(crop_right_rear, 0.5, crop_rear_right, 0.5, 0)  # overlap_right_rear

        return image_overlap

    def crop_image(self, image, x, y):
        img = cv2.circle(image.copy(), (x, y), 2, (200, 5, 200), -1)
        img = img[y - 70: (y - 70) + 140, x - 70:(x - 70) + 140]
        cv2.imwrite("img.jpg", img)
        return img

    def get_data_position(self, i_image, data):
        keys = list(self.model.properties_image)
        self.model.properties_image[keys[i_image]]["src"]["point1_x"] = data[0][0]
        self.model.properties_image[keys[i_image]]["src"]["point1_y"] = data[0][1]
        self.model.properties_image[keys[i_image]]["src"]["point2_x"] = data[1][0]
        self.model.properties_image[keys[i_image]]["src"]["point2_y"] = data[1][1]
        self.model.properties_image[keys[i_image]]["src"]["point3_x"] = data[2][0]
        self.model.properties_image[keys[i_image]]["src"]["point3_y"] = data[2][1]
        self.model.properties_image[keys[i_image]]["src"]["point4_x"] = data[3][0]
        self.model.properties_image[keys[i_image]]["src"]["point4_y"] = data[3][1]
        print(self.model.properties_image[keys[i_image]]["src"])

    def load_config_authentication(self, data_config):
        with open(data_config, "r") as file:
            data = yaml.safe_load(file)

        self.authen = data

    def authentication(self, password_in=None):
        if password_in is not None:
            self.authen["data"] = password_in
            password = password_in
        else:
            password = self.authen["data"]

        # result = os.system("echo '{}' | sudo -Si".format(str(password.strip())))  # important: strip() the newline char
        cmd = 'chmod -R 777 /opt/MoilDash'
        result = call('echo {} | sudo -S {}'.format(password, cmd), shell=True)

        if result == "0" or result == 0:
            status = True
        else:
            status = False
        return status

    def save_config_authentication(self, d_password, file):
        # encMessage = self.encrypting_data(d_password)
        # self.data = encMessage
        self.authen["data"] = d_password
        # file = self..app_ctxt.get_resource("data/data.yaml")
        with open(file, "w") as outfile:
            yaml.dump(self.authen, outfile, default_flow_style=False)
            print("save config success")