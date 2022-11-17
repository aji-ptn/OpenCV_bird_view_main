from .configuration_image_1 import ConfigurationImage1
from .configuration_image_2 import ConfigurationImage2
from .configuration_image_3 import ConfigurationImage3
from .configuration_image_4 import ConfigurationImage4
from .configuration_image_5 import ConfigurationImage5
from .configuration_image_6 import ConfigurationImage6
from .additional_function import select_file


class CalibProperties:
    def __init__(self, view_controller):
        self.view_controller = view_controller
        self.list_properties = []

        self.config_image_1 = ConfigurationImage1(self.view_controller)
        self.config_image_2 = ConfigurationImage2(self.view_controller)
        self.config_image_3 = ConfigurationImage3(self.view_controller)
        self.config_image_4 = ConfigurationImage4(self.view_controller)
        # self.config_image_5 = ConfigurationImage5(self.view_controller)
        # self.config_image_6 = ConfigurationImage6(self.view_controller)

        self.view_controller.main_ui.button_save_config.clicked.connect(self.save_data_configuration)
        self.view_controller.main_ui.button_load_config.clicked.connect(self.load_configuration)

    def save_data_configuration(self):
        self.view_controller.controller.save_config_to_file(self.view_controller.app_ctxt.get_resource("data_config"
                                                                                                      "/config.yaml"))

    def load_configuration(self):
        config_path = self.view_controller.app_ctxt.get_resource("data_config/config.yaml")
        # config_path = select_file(self.view_controller, "Select config !!", "../data_config",
        #                           "config file (*.yaml)")
        if config_path is not None:
            self.view_controller.controller.load_config(config_path)
            print(self.view_controller.model.properties_image)
            self.config_image_1.load_config_from_file()
            self.config_image_2.load_config_from_file()
            self.config_image_3.load_config_from_file()
            self.config_image_4.load_config_from_file()
            if self.view_controller.model.total_camera_used == 6:
                self.config_image_5.load_config_from_file()
                self.config_image_6.load_config_from_file()

    def set_intrinsic_parameter_to_ui(self):
        self.config_image_1.set_intrinsic_parameter_to_ui()
        self.config_image_2.set_intrinsic_parameter_to_ui()
        self.config_image_3.set_intrinsic_parameter_to_ui()
        self.config_image_4.set_intrinsic_parameter_to_ui()
        if self.view_controller.model.total_camera_used == 6:
            self.config_image_5.set_intrinsic_parameter_to_ui()
            self.config_image_6.set_intrinsic_parameter_to_ui()

    def update_config(self):
        self.config_image_1.update_properties_intrinsic()
        self.config_image_2.update_properties_intrinsic()
        self.config_image_3.update_properties_intrinsic()
        self.config_image_4.update_properties_intrinsic()
        if self.view_controller.model.total_camera_used == 6:
            self.config_image_5.update_properties_intrinsic()
            self.config_image_6.update_properties_intrinsic()

