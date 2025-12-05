import React from 'react';
import { useAuth } from '../../src/hooks/useAuth';

const SkillLevelContent = ({ children, level }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading personalized content...</div>;
  }

  if (!user || user.skill_level !== level) {
    return null;
  }

  return <>{children}</>;
};

export default SkillLevelContent;