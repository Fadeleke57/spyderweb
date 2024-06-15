import { StartScrape } from "@/components/StartScrape";
import Image from "next/image";
import cobweb from '../../public/cobweb.png';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="flex items-center space-x-4">
        <Image src={cobweb} alt="spyderweb icon" className="w-50 h-50" width={100} height={100} />
        <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">SpyderWeb</h1>
      </div>
      <StartScrape />
    </main>
  );
}