import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Foundations of Physical AI',
    emoji: '🤖',
    description: (
      <>
        Explore the fundamental concepts of physical AI and embodied intelligence.
        Learn how AI and robotics converge to create intelligent systems.
      </>
    ),
  },
  {
    title: 'Humanoid Robotics Engineering',
    emoji: '⚙️',
    description: (
      <>
        Delve into the engineering principles of humanoid robot design and control.
        Understand kinematics, dynamics, and locomotion.
      </>
    ),
  },
  {
    title: 'Intelligence & Learning',
    emoji: '🧠',
    description: (
      <>
        Explore AI for robotic learning, decision-making, and human-robot interaction.
        Discover how robots learn and adapt.
      </>
    ),
  },
];

function Feature({emoji, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className={styles.featureCard}>
        <div className={styles.featureIconWrapper}>
          <div className={styles.featureIcon}>{emoji}</div>
        </div>
        <div className={styles.featureContent}>
          <h3 className={styles.featureTitle}>{title}</h3>
          <p className={styles.featureDescription}>{description}</p>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

