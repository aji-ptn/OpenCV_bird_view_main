from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from .ui_py.main_ui import Ui_MainWindow
from .additional_function import select_file, init_ori_ratio, show_image_to_label
from .ui_authentication_controller import AuthenticationPassword
from .calib_properties import CalibProperties
from .show_to_windows import ShowToUi
from .additional_ui import AdditionalButton


class MainView(QMainWindow):
    def __init__(self, parent, appctxt, model, controller):
        super(MainView, self).__init__()
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(parent)

        self.model = model
        self.controller = controller
        self.appctxt = appctxt
        self.additional_button = AdditionalButton(self)
        # self.additional_button
        self.config_path_authentication = self.appctxt.get_resource('data/data.yaml')
        self.calib_properties = CalibProperties(self)
        self.show_to_ui = ShowToUi(self)
        self.main_ui.wind_show_undistortion_point.setMouseTracking(True)

        self.list_btn_point = [self.main_ui.button_select_point_0, self.main_ui.button_select_point_1,
                               self.main_ui.button_select_point_2, self.main_ui.button_select_point_3]
        self.list_add_value_src_to_ui = [self.calib_properties.config_image_1,
                                         self.calib_properties.config_image_2,
                                         self.calib_properties.config_image_3,
                                         self.calib_properties.config_image_4]
        self.data = []

        self.hide()
        self.add_label_zoom()
        self.connect()

    def hide(self):
        self.main_ui.toolBox.setItemEnabled(4, False)
        self.main_ui.toolBox.setItemEnabled(5, False)
        self.main_ui.label_38.hide()
        self.main_ui.spinBox_shift_x_1.hide()
        self.main_ui.label_40.hide()
        self.main_ui.spinBox_shift_y_1.hide()
        self.main_ui.label_41.hide()
        self.main_ui.spinBox_shift_x_2.hide()
        self.main_ui.label_42.hide()
        self.main_ui.spinBox_shift_y_2.hide()
        self.main_ui.label_219.hide()
        self.main_ui.spinBox_shift_x_3.hide()
        self.main_ui.label_220.hide()
        self.main_ui.spinBox_shift_y_3.hide()
        self.main_ui.label_223.hide()
        self.main_ui.spinBox_shift_x_5.hide()
        self.main_ui.label_224.hide()
        self.main_ui.spinBox_shift_y_5.hide()

    def connect(self):
        self.main_ui.button_open_image.clicked.connect(self.open_image)
        self.main_ui.toolBox.currentChanged.connect(self.activate_toolbox)
        self.main_ui.checkBox_show_overlapping.clicked.connect(self.change_overlap_or_bird_view)
        self.main_ui.wind_show_undistortion_point.mouseMoveEvent = self.mouse_event_move
        # self.main_ui.wind_show_undistortion_point.mousePressEvent = self.mouse_event_click
        self.main_ui.wind_show_undistortion_point.mousePressEvent = self.get_position_in_image

        self.main_ui.button_select_point_0.clicked.connect(lambda: self.onclick_select_point(0))
        self.main_ui.button_select_point_1.clicked.connect(lambda: self.onclick_select_point(1))
        self.main_ui.button_select_point_2.clicked.connect(lambda: self.onclick_select_point(2))
        self.main_ui.button_select_point_3.clicked.connect(lambda: self.onclick_select_point(3))

        self.main_ui.button_clear_0.clicked.connect(self.onclick_clear_point)
        self.main_ui.button_clear_1.clicked.connect(self.onclick_clear_point)
        self.main_ui.button_clear_2.clicked.connect(self.onclick_clear_point)
        self.main_ui.button_clear_3.clicked.connect(self.onclick_clear_point)

        # self.wind_undistortion_left.wheelEvent = self.mouse_event.mouse_wheelEvent_left

    def open_image(self):
        self.model.total_camera_used = 4
        self.check_authentication()
        self.controller.initial_properties()
        self.calib_properties.update_config()
        QMessageBox.information(None, "Information", "Select Source and parameter Image\nImage front -> left -> right "
                                                     "-> rear")
        for i in range(self.model.total_camera_used):
            path_image = select_file(None, "Select image !", "../", "Image file (*.jpeg *.jpg *.png)")

            if path_image:
                path_parameter = select_file(None, "Select Parameter !", "../", "Parameter Files (*.yaml)")

                if path_parameter:
                    self.controller.list_intrinsic_data(path_parameter)
                    self.controller.list_image_data(path_image, i)
                    if self.controller.data_config is None:
                        self.controller.update_intrinsic_parameter(i)
                    self.controller.process_undistorted_image(i)
                    self.controller.process_perspective_image(i)
                    self.show_to_ui.show_union_original_image()
                    self.show_to_ui.show_image_current_calib()
        try:
            self.controller.process_bird_view("bird_view")
            self.show_to_ui.show_bird_view_image()
        except:
            pass
        self.calib_properties.set_intrinsic_parameter_to_ui()
        print(self.model.properties_image)

    def check_authentication(self):
        self.controller.load_config_authentication(self.config_path_authentication)
        status = self.controller.authentication()
        if not status:
            auth_config = QtWidgets.QDialog()
            source_cam = AuthenticationPassword(auth_config, self)
            auth_config.exec()
            if source_cam is not None:
                status = self.controller.authentication(source_cam.password)
                if status:
                    self.controller.save_config_authentication(source_cam.password, self.config_path_authentication)
                    print("done")

    def activate_toolbox(self):
        index = self.main_ui.toolBox.currentIndex()
        print(index)
        try:
            if self.model.list_original_image:
                self.show_to_ui.show_image_current_calib()
        except:
            print("pass")

    def change_overlap_or_bird_view(self):
        if self.main_ui.checkBox_show_overlapping.isChecked():
            self.controller.process_bird_view("overlap")
        else:
            self.controller.process_bird_view("bird_view")
        self.show_to_ui.show_bird_view_image()

    def add_label_zoom(self):
        self.add_label = QLabel(self.main_ui.wind_show_undistortion_point)
        self.add_label.setGeometry(QtCore.QRect(5, 5, 100, 100))
        self.add_label.setFrameShape(QLabel.Shape.Box)
        self.add_label.setFrameShadow(QLabel.Shadow.Raised)
        self.add_label.hide()

    # def mouse_event_click(self, e):
    #     if e.button() == QtCore.Qt.MouseButton.LeftButton:
    #         pos_x = round(e.x())
    #         pos_y = round(e.y())
    #         print(pos_x, pos_y)

    def mouse_event_move(self, e):
        index = self.main_ui.toolBox.currentIndex()
        pos_x = round(e.x())
        pos_y = round(e.y())
        try:
            image_undistorted = self.model.list_undistorted_drawing_image[index]
        except:
            image_undistorted = None
        if image_undistorted is not None:
            ratio_x, ratio_y = init_ori_ratio(self.main_ui.wind_show_undistortion_point, image_undistorted)
            X = round(pos_x * ratio_x)
            Y = round(pos_y * ratio_y)
            try:
                if X > 70 and Y > 70:
                    self.add_label.show()
                    self.add_label.setGeometry(QtCore.QRect(pos_x + 15, pos_y - 15, 100, 100))
                    if self.main_ui.wind_show_undistortion_point.height() - pos_y < 200:
                        self.add_label.setGeometry(QtCore.QRect(pos_x + 15, pos_y - 150, 100, 100))

                    if self.main_ui.wind_show_undistortion_point.width() - pos_x < 200:
                        self.add_label.setGeometry(QtCore.QRect(pos_x - 150, pos_y + 15, 100, 100))

                    if self.main_ui.wind_show_undistortion_point.height() - pos_y < 200 and self.main_ui. \
                            wind_show_undistortion_point.width() - pos_x < 200:
                        self.add_label.setGeometry(QtCore.QRect(pos_x - 150, pos_y - 150, 100, 100))

                    if self.main_ui.wind_show_undistortion_point.height() - pos_y < 20 and self.main_ui. \
                            wind_show_undistortion_point.width() - pos_x < 20:
                        self.add_label.hide()

                    img = self.controller.crop_image(image_undistorted, X, Y)
                    # image_ = cv2.circle(self.image.copy(), (X, Y), 2, (200, 5, 200), -1)
                    # image = image_undistorted.copy()[Y - 70: (Y - 70) + 140, X - 70:(X - 70) + 140]
                    # self.show_to_ui.show_image_point_selection(self.add_label, image, 140)
                    show_image_to_label(self.add_label, img, 140)

                else:
                    self.add_label.hide()
            except:
                pass

    def get_position_in_image(self, e):
        print("here")
        # data = []
        index = self.main_ui.toolBox.currentIndex()
        ratio_x, ratio_y = init_ori_ratio(self.main_ui.wind_show_undistortion_point,
                                          self.model.list_undistorted_drawing_image[index])
        if e.button() == Qt.LeftButton:
            pos_x = round(e.x() * ratio_x)
            pos_y = round(e.y() * ratio_y)
            if self.list_btn_point[index].isChecked():
                coordinate = [pos_x, pos_y]
                self.data.append(coordinate)
                if len(self.data) == 4:
                    print(self.data)
                    self.disable_button_select_point()
                    self.controller.get_data_position(index, self.data)
                    self.list_add_value_src_to_ui[index].set_properties_src_to_ui()

    def disable_button_select_point(self):
        self.main_ui.button_select_point_0.setChecked(False)
        self.main_ui.button_select_point_1.setChecked(False)
        self.main_ui.button_select_point_2.setChecked(False)
        self.main_ui.button_select_point_3.setChecked(False)

    def onclick_select_point(self, i):
        self.list_btn_point[i].setChecked(True)
        self.data = []

    def onclick_clear_point(self):
        index = self.main_ui.toolBox.currentIndex()
        self.data = []
        for ih in range(4):
            self.data.append([0, 0])
        self.controller.get_data_position(index, self.data)
        self.list_add_value_src_to_ui[index].set_properties_src_to_ui()
