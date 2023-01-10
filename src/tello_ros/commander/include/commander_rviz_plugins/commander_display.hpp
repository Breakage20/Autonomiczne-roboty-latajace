// Copyright 2022 Borong Yuan
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#pragma once

#ifndef Q_MOC_RUN

#include <OgreCamera.h>
#include <OgreColourValue.h>

#include "rviz_common/display.hpp"
#include "rviz_common/display_context.hpp"
#include "rviz_common/panel_dock_widget.hpp"
#include "rviz_common/render_panel.hpp"
#include "rviz_common/view_manager.hpp"
#include "rviz_common/properties/float_property.hpp"
#include "rviz_rendering/logging.hpp"
#include "rviz_rendering/render_window.hpp"
#include <QPushButton>
#include <QtWidgets>
#include <QGridLayout>

#endif

namespace commander_rviz_plugins
{
    class CommanderDisplay : public rviz_common::Display
    {
        Q_OBJECT

    public:
        CommanderDisplay();
        ~CommanderDisplay();


    private Q_SLOTS:
        void onButton1Clicked(){RCLCPP_INFO(node->get_logger(),"Dupa");};
        void onButton2Clicked();
        void onButton3Clicked();
        void onButton4Clicked();

    protected:
        void onInitialize() override;

    private:    
        int win_x_{640}, win_y_{480}, win_w_{640}, win_h_{480}, tile_x_{0}, tile_y_{1};

        rclcpp::Node *node = new rclcpp::Node("minimal_publisher");

        std::unique_ptr<QPushButton> button1_;
        std::unique_ptr<QPushButton> button2_;
        std::unique_ptr<QPushButton> button3_;
        std::unique_ptr<QPushButton> button4_;

        rviz_common::properties::FloatProperty *near_clip_property_;
        rviz_common::properties::FloatProperty *far_clip_property_;

        std::unique_ptr<rviz_common::RenderPanel> commander_panel_;
        rviz_common::PanelDockWidget *looking_commander_panel_;

        void initializeLookingGlass();
        void initializeButtons();
        void setupCommanderPanel();
        void setupLookingCommanderPanel();
    };
} // namespace commander_rviz_plugins
