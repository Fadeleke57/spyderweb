import React from 'react';
import StartScraping from './StartScraping';
import GraphDisplay from './Graph';
import styles from './page.module.css'

const Home: React.FC = () => {
  return (
    <div className={styles.main}>
      <h1>SpyderWeb Beta</h1>
      <StartScraping />
      <GraphDisplay />
    </div>
  );
};

export default Home;