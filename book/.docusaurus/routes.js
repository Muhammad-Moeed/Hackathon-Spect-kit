import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/Hackathon-Spect-kit/__docusaurus/debug',
    component: ComponentCreator('/Hackathon-Spect-kit/__docusaurus/debug', '48e'),
    exact: true
  },
  {
    path: '/Hackathon-Spect-kit/__docusaurus/debug/config',
    component: ComponentCreator('/Hackathon-Spect-kit/__docusaurus/debug/config', '347'),
    exact: true
  },
  {
    path: '/Hackathon-Spect-kit/__docusaurus/debug/content',
    component: ComponentCreator('/Hackathon-Spect-kit/__docusaurus/debug/content', '810'),
    exact: true
  },
  {
    path: '/Hackathon-Spect-kit/__docusaurus/debug/globalData',
    component: ComponentCreator('/Hackathon-Spect-kit/__docusaurus/debug/globalData', 'a87'),
    exact: true
  },
  {
    path: '/Hackathon-Spect-kit/__docusaurus/debug/metadata',
    component: ComponentCreator('/Hackathon-Spect-kit/__docusaurus/debug/metadata', '1f2'),
    exact: true
  },
  {
    path: '/Hackathon-Spect-kit/__docusaurus/debug/registry',
    component: ComponentCreator('/Hackathon-Spect-kit/__docusaurus/debug/registry', 'fb7'),
    exact: true
  },
  {
    path: '/Hackathon-Spect-kit/__docusaurus/debug/routes',
    component: ComponentCreator('/Hackathon-Spect-kit/__docusaurus/debug/routes', '32f'),
    exact: true
  },
  {
    path: '/Hackathon-Spect-kit/login',
    component: ComponentCreator('/Hackathon-Spect-kit/login', '75b'),
    exact: true
  },
  {
    path: '/Hackathon-Spect-kit/profile',
    component: ComponentCreator('/Hackathon-Spect-kit/profile', '1c0'),
    exact: true
  },
  {
    path: '/Hackathon-Spect-kit/signup',
    component: ComponentCreator('/Hackathon-Spect-kit/signup', '1af'),
    exact: true
  },
  {
    path: '/Hackathon-Spect-kit/docs',
    component: ComponentCreator('/Hackathon-Spect-kit/docs', '771'),
    routes: [
      {
        path: '/Hackathon-Spect-kit/docs',
        component: ComponentCreator('/Hackathon-Spect-kit/docs', '797'),
        routes: [
          {
            path: '/Hackathon-Spect-kit/docs',
            component: ComponentCreator('/Hackathon-Spect-kit/docs', 'f1f'),
            routes: [
              {
                path: '/Hackathon-Spect-kit/docs/category/applications-future',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/category/applications-future', '6f2'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/category/foundations',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/category/foundations', 'b04'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/category/intelligence-learning',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/category/intelligence-learning', '79f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/category/robotics-engineering',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/category/robotics-engineering', '5cd'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/intro',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/intro', '076'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module1/basic_ai_concepts',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module1/basic_ai_concepts', '6da'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module1/embodied_intelligence',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module1/embodied_intelligence', 'cdf'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module1/introduction',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module1/introduction', '252'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module1/robot_hardware_overview',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module1/robot_hardware_overview', '8eb'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module2/actuator_control',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module2/actuator_control', '12d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module2/humanoid_design_principles',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module2/humanoid_design_principles', '6db'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module2/kinematics_dynamics',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module2/kinematics_dynamics', 'c9f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module2/locomotion_balance',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module2/locomotion_balance', 'e9a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module3/decision_making_planning',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module3/decision_making_planning', '50f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module3/human_robot_interaction',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module3/human_robot_interaction', '7d7'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module3/robot_learning_paradigms',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module3/robot_learning_paradigms', 'd22'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module3/social_ethical_implications',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module3/social_ethical_implications', '705'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module4/emerging_trends',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module4/emerging_trends', 'fdf'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module4/future_challenges',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module4/future_challenges', 'c02'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module4/real_world_applications',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module4/real_world_applications', '492'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Spect-kit/docs/module4/societal_impact_ethics',
                component: ComponentCreator('/Hackathon-Spect-kit/docs/module4/societal_impact_ethics', '272'),
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
    path: '/Hackathon-Spect-kit/',
    component: ComponentCreator('/Hackathon-Spect-kit/', '031'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
