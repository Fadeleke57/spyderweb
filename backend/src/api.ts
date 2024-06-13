import express from 'express';
import { spawn } from 'child_process';
import dotenv from 'dotenv';

dotenv.config();

const router = express.Router();

router.post('/start-scraping', (req, res) => {
  const { searchTerm } = req.body;
  if (!searchTerm) {
    return res.status(400).json({ message: 'searchTerm is required' });
  }

  const scrapyProcess = spawn('scrapy', ['crawl', 'time', '-a', `search_term=${searchTerm}`], {
    cwd: process.env.SCRAPY_PROJECT_DIR,
    shell: true,
  });

  let processOutput = ''; //output of scrapy process

  scrapyProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
    processOutput += data.toString();
  });

  scrapyProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
    processOutput += data.toString();
  });

  scrapyProcess.on('close', (code) => { //scrapy process done
    console.log(`child process exited with code ${code}`);
    if (!res.headersSent) {  //avoid sending response if headers have already been sent
      if (code === 0) {
        res.status(200).json({ message: 'Scraping process started successfully', output: processOutput });
      } else {
        res.status(500).json({ message: 'Failed to start scraping process', output: processOutput });
      }
    }
  });

  scrapyProcess.on('error', (error) => { //scrapy process error
    console.error(`error: ${error.message}`);
    if (!res.headersSent) { //avoid sending response if headers have already been sent
      res.status(500).json({ message: 'Failed to start scraping process', error: error.message });
    }
  });
});

export default router;