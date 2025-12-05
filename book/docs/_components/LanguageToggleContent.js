import React from 'react';
import { useAuth } from '../../src/hooks/useAuth';

const LanguageToggleContent = ({ children, lang }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading language-specific content...</div>;
  }

  if (!user || user.preferred_language !== lang) {
    return null;
  }

  return <>{children}</>;
};

export default LanguageToggleContent;