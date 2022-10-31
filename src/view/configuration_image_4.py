class ConfigurationImage4:
    def __init__(self, view_controller):
        self.view_controller = view_controller

        self.connect_action()

    def connect_action(self):
        # ================== intrinsic parameter ==================
        self.view_controller.main_ui.doubleSpinBox_fx_3.valueChanged.connect(self.change_intrinsic_from_ui)
        self.view_controller.main_ui.doubleSpinBox_fy_3.valueChanged.connect(self.change_intrinsic_from_ui)
        self.view_controller.main_ui.doubleSpinBox_icx_3.valueChanged.connect(self.change_intrinsic_from_ui)
        self.view_controller.main_ui.doubleSpinBox_icy_3.valueChanged.connect(self.change_intrinsic_from_ui)
        self.view_controller.main_ui.spinBox_width_3.valueChanged.connect(self.change_intrinsic_from_ui)
        self.view_controller.main_ui.spinBox_height_3.valueChanged.connect(self.change_intrinsic_from_ui)

        # ================== src parameter ==================
        self.view_controller.main_ui.spinBox_src_point1_x_3.valueChanged.connect(self.change_properties_src_from_ui)
        self.view_controller.main_ui.spinBox_src_point1_y_3.valueChanged.connect(self.change_properties_src_from_ui)
        self.view_controller.main_ui.spinBox_src_point2_x_3.valueChanged.connect(self.change_properties_src_from_ui)
        self.view_controller.main_ui.spinBox_src_point2_y_3.valueChanged.connect(self.change_properties_src_from_ui)
        self.view_controller.main_ui.spinBox_src_point3_x_3.valueChanged.connect(self.change_properties_src_from_ui)
        self.view_controller.main_ui.spinBox_src_point3_y_3.valueChanged.connect(self.change_properties_src_from_ui)
        self.view_controller.main_ui.spinBox_src_point4_x_3.valueChanged.connect(self.change_properties_src_from_ui)
        self.view_controller.main_ui.spinBox_src_point4_y_3.valueChanged.connect(self.change_properties_src_from_ui)

        # ================== dst parameter ==================
        self.view_controller.main_ui.spinBox_dst_point1_x_3.valueChanged.connect(self.change_properties_dst_from_ui)
        self.view_controller.main_ui.spinBox_dst_point1_y_3.valueChanged.connect(self.change_properties_dst_from_ui)
        self.view_controller.main_ui.spinBox_dst_point2_x_3.valueChanged.connect(self.change_properties_dst_from_ui)
        self.view_controller.main_ui.spinBox_dst_point2_y_3.valueChanged.connect(self.change_properties_dst_from_ui)
        self.view_controller.main_ui.spinBox_dst_point3_x_3.valueChanged.connect(self.change_properties_dst_from_ui)
        self.view_controller.main_ui.spinBox_dst_point3_y_3.valueChanged.connect(self.change_properties_dst_from_ui)
        self.view_controller.main_ui.spinBox_dst_point4_x_3.valueChanged.connect(self.change_properties_dst_from_ui)
        self.view_controller.main_ui.spinBox_dst_point4_y_3.valueChanged.connect(self.change_properties_dst_from_ui)
        self.view_controller.main_ui.spinBox_width_dst_3.valueChanged.connect(self.change_properties_dst_from_ui)
        self.view_controller.main_ui.spinBox_height_dst_3.valueChanged.connect(self.change_properties_dst_from_ui)

    def update_properties_intrinsic(self):
        self.view_controller.model.properties_image["Image_4"] = {}
        self.view_controller.model.properties_image["Image_4"]["Ins"] = {}
        self.update_properties_src()
        self.update_properties_dst()
        self.change_properties_intrinsic()

    def update_properties_src(self):
        self.view_controller.model.properties_image["Image_4"]["src"] = {}
        self.change_properties_src()

    def update_properties_dst(self):
        self.view_controller.model.properties_image["Image_4"]["dst"] = {}
        self.change_properties_dst()

    def change_intrinsic_from_ui(self):
        self.change_properties_intrinsic()
        index = self.view_controller.main_ui.toolBox.currentIndex()
        self.view_controller.controller.process_perspective_image(index)
        self.view_controller.show_to_ui.show_image_current_calib()

    def change_properties_src_from_ui(self):
        self.change_properties_src()
        index = self.view_controller.main_ui.toolBox.currentIndex()
        self.view_controller.controller.process_perspective_image(index)
        self.view_controller.show_to_ui.show_image_current_calib()

    def change_properties_dst_from_ui(self):
        self.change_properties_dst()
        index = self.view_controller.main_ui.toolBox.currentIndex()
        self.view_controller.controller.process_perspective_image(index)
        self.view_controller.show_to_ui.show_image_current_calib()

    def load_config_from_file(self):
        self.set_intrinsic_parameter_to_ui()
        self.set_properties_src_to_ui()
        self.set_properties_dst_to_ui()

    def change_properties_intrinsic(self):
        self.view_controller.model.properties_image["Image_4"]["Ins"][
            "Fx"] = self.view_controller.main_ui.doubleSpinBox_fx_3.value()
        self.view_controller.model.properties_image["Image_4"]["Ins"][
            "Fy"] = self.view_controller.main_ui.doubleSpinBox_fy_3.value()
        self.view_controller.model.properties_image["Image_4"]["Ins"][
            "Icx"] = self.view_controller.main_ui.doubleSpinBox_icx_3.value()
        self.view_controller.model.properties_image["Image_4"]["Ins"][
            "Icy"] = self.view_controller.main_ui.doubleSpinBox_icy_3.value()
        self.view_controller.model.properties_image["Image_4"]["Ins"][
            "Width"] = self.view_controller.main_ui.spinBox_width_3.value()
        self.view_controller.model.properties_image["Image_4"]["Ins"][
            "Height"] = self.view_controller.main_ui.spinBox_height_3.value()

    def change_properties_src(self):
        self.view_controller.model.properties_image["Image_4"]["src"][
            "point1_x"] = self.view_controller.main_ui.spinBox_src_point1_x_3.value()
        self.view_controller.model.properties_image["Image_4"]["src"][
            "point1_y"] = self.view_controller.main_ui.spinBox_src_point1_y_3.value()
        self.view_controller.model.properties_image["Image_4"]["src"][
            "point2_x"] = self.view_controller.main_ui.spinBox_src_point2_x_3.value()
        self.view_controller.model.properties_image["Image_4"]["src"][
            "point2_y"] = self.view_controller.main_ui.spinBox_src_point2_y_3.value()
        self.view_controller.model.properties_image["Image_4"]["src"][
            "point3_x"] = self.view_controller.main_ui.spinBox_src_point3_x_3.value()
        self.view_controller.model.properties_image["Image_4"]["src"][
            "point3_y"] = self.view_controller.main_ui.spinBox_src_point3_y_3.value()
        self.view_controller.model.properties_image["Image_4"]["src"][
            "point4_x"] = self.view_controller.main_ui.spinBox_src_point4_x_3.value()
        self.view_controller.model.properties_image["Image_4"]["src"][
            "point4_y"] = self.view_controller.main_ui.spinBox_src_point4_y_3.value()

    def change_properties_dst(self):
        self.view_controller.model.properties_image["Image_4"]["dst"][
            "point1_x"] = self.view_controller.main_ui.spinBox_dst_point1_x_3.value()
        self.view_controller.model.properties_image["Image_4"]["dst"][
            "point1_y"] = self.view_controller.main_ui.spinBox_dst_point1_y_3.value()
        self.view_controller.model.properties_image["Image_4"]["dst"][
            "point2_x"] = self.view_controller.main_ui.spinBox_dst_point2_x_3.value()
        self.view_controller.model.properties_image["Image_4"]["dst"][
            "point2_y"] = self.view_controller.main_ui.spinBox_dst_point2_y_3.value()
        self.view_controller.model.properties_image["Image_4"]["dst"][
            "point3_x"] = self.view_controller.main_ui.spinBox_dst_point3_x_3.value()
        self.view_controller.model.properties_image["Image_4"]["dst"][
            "point3_y"] = self.view_controller.main_ui.spinBox_dst_point3_y_3.value()
        self.view_controller.model.properties_image["Image_4"]["dst"][
            "point4_x"] = self.view_controller.main_ui.spinBox_dst_point4_x_3.value()
        self.view_controller.model.properties_image["Image_4"]["dst"][
            "point4_y"] = self.view_controller.main_ui.spinBox_dst_point4_y_3.value()
        self.view_controller.model.properties_image["Image_4"]["dst"][
            "Width"] = self.view_controller.main_ui.spinBox_width_dst_3.value()
        self.view_controller.model.properties_image["Image_4"]["dst"][
            "Height"] = self.view_controller.main_ui.spinBox_height_dst_3.value()

    def set_intrinsic_parameter_to_ui(self):
        self.block_signal_intrinsic_param()
        self.view_controller.main_ui.doubleSpinBox_fx_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["Ins"]["Fx"])
        self.view_controller.main_ui.doubleSpinBox_fy_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["Ins"]["Fy"])
        self.view_controller.main_ui.doubleSpinBox_icx_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["Ins"]["Icx"])
        self.view_controller.main_ui.doubleSpinBox_icy_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["Ins"]["Icy"])
        self.view_controller.main_ui.spinBox_width_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["Ins"]["Width"])
        self.view_controller.main_ui.spinBox_height_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["Ins"]["Height"])
        self.unblock_signal_intrinsic_param()

    def set_properties_src_to_ui(self):
        self.block_signal_src()
        self.view_controller.main_ui.spinBox_src_point1_x_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["src"]["point1_x"])
        self.view_controller.main_ui.spinBox_src_point1_y_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["src"]["point1_y"])
        self.view_controller.main_ui.spinBox_src_point2_x_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["src"]["point2_x"])
        self.view_controller.main_ui.spinBox_src_point2_y_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["src"]["point2_y"])
        self.view_controller.main_ui.spinBox_src_point3_x_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["src"]["point3_x"])
        self.view_controller.main_ui.spinBox_src_point3_y_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["src"]["point3_y"])
        self.view_controller.main_ui.spinBox_src_point4_x_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["src"]["point4_x"])
        self.view_controller.main_ui.spinBox_src_point4_y_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["src"]["point4_y"])
        self.unblock_signal_src()

    def set_properties_dst_to_ui(self):
        self.block_signal_dst()
        self.view_controller.main_ui.spinBox_dst_point1_x_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["dst"]["point1_x"])
        self.view_controller.main_ui.spinBox_dst_point1_y_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["dst"]["point1_y"])
        self.view_controller.main_ui.spinBox_dst_point2_x_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["dst"]["point2_x"])
        self.view_controller.main_ui.spinBox_dst_point2_y_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["dst"]["point2_y"])
        self.view_controller.main_ui.spinBox_dst_point3_x_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["dst"]["point3_x"])
        self.view_controller.main_ui.spinBox_dst_point3_y_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["dst"]["point3_y"])
        self.view_controller.main_ui.spinBox_dst_point4_x_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["dst"]["point4_x"])
        self.view_controller.main_ui.spinBox_dst_point4_y_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["dst"]["point4_y"])
        self.view_controller.main_ui.spinBox_width_dst_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["dst"]["Width"])
        self.view_controller.main_ui.spinBox_height_dst_3.setValue(
            self.view_controller.model.properties_image["Image_4"]["dst"]["Height"])
        self.unblock_signal_dst()

    def block_signal_intrinsic_param(self):
        self.view_controller.main_ui.doubleSpinBox_fx_3.blockSignals(True)
        self.view_controller.main_ui.doubleSpinBox_fy_3.blockSignals(True)
        self.view_controller.main_ui.doubleSpinBox_icx_3.blockSignals(True)
        self.view_controller.main_ui.doubleSpinBox_icy_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_width_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_height_3.blockSignals(True)

    def unblock_signal_intrinsic_param(self):
        self.view_controller.main_ui.doubleSpinBox_fx_3.blockSignals(False)
        self.view_controller.main_ui.doubleSpinBox_fy_3.blockSignals(False)
        self.view_controller.main_ui.doubleSpinBox_icx_3.blockSignals(False)
        self.view_controller.main_ui.doubleSpinBox_icy_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_width_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_height_3.blockSignals(False)

    def block_signal_src(self):
        self.view_controller.main_ui.spinBox_src_point1_x_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_src_point1_y_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_src_point2_x_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_src_point2_y_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_src_point3_x_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_src_point3_y_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_src_point4_x_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_src_point4_y_3.blockSignals(True)

    def unblock_signal_src(self):
        self.view_controller.main_ui.spinBox_src_point1_x_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_src_point1_y_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_src_point2_x_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_src_point2_y_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_src_point3_x_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_src_point3_y_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_src_point4_x_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_src_point4_y_3.blockSignals(False)

    def block_signal_dst(self):
        self.view_controller.main_ui.spinBox_dst_point1_x_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_dst_point1_y_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_dst_point2_x_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_dst_point2_y_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_dst_point3_x_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_dst_point3_y_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_dst_point4_x_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_dst_point4_y_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_width_dst_3.blockSignals(True)
        self.view_controller.main_ui.spinBox_height_dst_3.blockSignals(True)

    def unblock_signal_dst(self):
        self.view_controller.main_ui.spinBox_dst_point1_x_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_dst_point1_y_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_dst_point2_x_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_dst_point2_y_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_dst_point3_x_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_dst_point3_y_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_dst_point4_x_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_dst_point4_y_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_width_dst_3.blockSignals(False)
        self.view_controller.main_ui.spinBox_height_dst_3.blockSignals(False)
