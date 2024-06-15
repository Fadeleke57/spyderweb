import React from 'react';
import StartScraping from './StartScraping';
import GraphDisplay from './Graph';
import styles from './page.module.css'
import { Toaster } from 'react-hot-toast';
import Link from 'next/link';

const Home: React.FC = () => {
  return (
    <>
      <Toaster/>
      <div className={styles.main}>
        <h1>SpyderWeb Beta</h1>
        <Link href={"/pages/docs"}>Docs</Link>
        <StartScraping />
        <GraphDisplay />
      </div>
    </>

  );
};

export default Home;