import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/Hackathon-Spect-kit/book/login',
    component: ComponentCreator('/Hackathon-Spect-kit/book/login', '28a'),
    exact: true
  },
  {
    path: '/Hackathon-Spect-kit/book/profile',
    component: ComponentCreator('/Hackathon-Spect-kit/book/profile', '245'),
    exact: true
  },
  {
    path: '/Hackathon-Spect-kit/book/signup',
    component: ComponentCreator('/Hackathon-Spect-kit/book/signup', '88e'),
    exact: true
  },
  {
    path: '/Hackathon-Spect-kit/book/docs',
    component: ComponentCreator('/Hackathon-Spect-kit/book/docs', '0d2'),
    routes: [
      {
        path: '/Hackathon-Spect-kit/book/docs',
        component: ComponentCreator('/Hackathon-Spect-kit/book/docs', '53e'),
        routes: [
          {
            path: '/Hackathon-Spect-kit/book/docs',
            component: ComponentCreator('/Hackathon-Spect-kit/book/docs', '4bd'),
            routes: [
              {
                path: '/Hackathon-Spect-kit/book/docs/category/applications-future',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/category/applications-future', '556'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/category/foundations',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/category/foundations', 'a42'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/category/intelligence-learning',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/category/intelligence-learning', 'a26'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/category/robotics-engineering',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/category/robotics-engineering', '947'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/intro',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/intro', 'fb7'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module1/basic_ai_concepts',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module1/basic_ai_concepts', 'af5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module1/embodied_intelligence',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module1/embodied_intelligence', '409'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module1/introduction',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module1/introduction', '9a0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module1/robot_hardware_overview',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module1/robot_hardware_overview', 'dea'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module2/actuator_control',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module2/actuator_control', '7c2'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module2/humanoid_design_principles',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module2/humanoid_design_principles', '34d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module2/kinematics_dynamics',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module2/kinematics_dynamics', '7f7'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module2/locomotion_balance',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module2/locomotion_balance', '817'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module3/decision_making_planning',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module3/decision_making_planning', 'a56'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module3/human_robot_interaction',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module3/human_robot_interaction', '6f5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module3/robot_learning_paradigms',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module3/robot_learning_paradigms', 'd8c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module3/social_ethical_implications',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module3/social_ethical_implications', '6a7'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module4/emerging_trends',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module4/emerging_trends', 'c90'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module4/future_challenges',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module4/future_challenges', 'd96'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module4/real_world_applications',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module4/real_world_applications', '9fa'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/book/docs/module4/societal_impact_ethics',
                component: ComponentCreator('/Hackathon-Spect-kit/book/docs/module4/societal_impact_ethics', 'a84'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/Hackathon-Spect-kit/book/',
    component: ComponentCreator('/Hackathon-Spect-kit/book/', '423'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
