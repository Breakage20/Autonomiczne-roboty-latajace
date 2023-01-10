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
#include <iostream>
#include "commander_rviz_plugins/commander_display.hpp"

namespace commander_rviz_plugins
{
    using rviz_common::properties::StatusLevel;

    CommanderDisplay::CommanderDisplay()
    {
        near_clip_property_ = new rviz_common::properties::FloatProperty("Near Clip", 0.0, "", this);

        far_clip_property_ = new rviz_common::properties::FloatProperty("Far Clip", 0.0, "", this);
    }

    CommanderDisplay::~CommanderDisplay()
    {

    }
    void CommanderDisplay::onInitialize()
    {
        try
        {
            setupCommanderPanel();
            initializeButtons();
            setupLookingCommanderPanel();

            setStatus(StatusLevel::Ok, "DD", "OK");
        }
        catch (const std::exception &e)
        {
            setStatus(StatusLevel::Error, "DD", e.what());
        }
    }
    void CommanderDisplay::initializeButtons()
    {
        button1_ = std::make_unique<QPushButton>("Button 1");
        button2_ = std::make_unique<QPushButton>("Button 2");
        button3_ = std::make_unique<QPushButton>("Button 3");
        button4_ = std::make_unique<QPushButton>("Button 4");

        connect(button1_.get(), &QPushButton::clicked, this, &CommanderDisplay::onButton1Clicked);
        connect(button2_.get(), &QPushButton::clicked, this, &CommanderDisplay::onButton1Clicked);
        connect(button3_.get(), &QPushButton::clicked, this, &CommanderDisplay::onButton1Clicked);
        connect(button4_.get(), &QPushButton::clicked, this, &CommanderDisplay::onButton1Clicked);
    }

    void CommanderDisplay::setupCommanderPanel()
    {
        commander_panel_ = std::make_unique<rviz_common::RenderPanel>();
        commander_panel_->initialize(context_, true);
        setAssociatedWidget(commander_panel_.get());

        static int count = 0;
        commander_panel_->getRenderWindow()->setObjectName("CommanderPlayRenderWindow" + QString::number(count++));
        commander_panel_->setViewController(context_->getViewManager()->getCurrent());
    }

    void CommanderDisplay::setupLookingCommanderPanel()
    {
        QWidget *q = new QWidget;
        QGridLayout *mainLayout = new QGridLayout;
        mainLayout->addWidget(button1_.get(),0,0,1,1);
        mainLayout->addWidget(button2_.get(),0,1,1,1);
        mainLayout->addWidget(button3_.get(),0,2,1,1);
        mainLayout->addWidget(button4_.get(),0,3,1,1);
        q->setLayout(mainLayout);
        //commander_panel_->setLayout(mainLayout);
        looking_commander_panel_ = getAssociatedWidgetPanel();
        looking_commander_panel_->setContentWidget(q);  //(new QWidget(looking_commander_panel_));
        looking_commander_panel_->setFloating(true);
        looking_commander_panel_->setGeometry(win_x_, win_y_, win_w_, win_h_);
        looking_commander_panel_->setWindowState(looking_commander_panel_->windowState() | Qt::WindowNoState);
    }
} // namespace commander_rviz_plugins

#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(commander_rviz_plugins::CommanderDisplay, rviz_common::Display)
