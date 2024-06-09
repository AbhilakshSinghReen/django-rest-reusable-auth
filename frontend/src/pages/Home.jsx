import { useEffect } from "react";

import { appName } from "../config/config";

export default function Home() {
  useEffect(() => {
    document.title = appName;
  }, []);

  return (
    <div>
      <h1>{appName}</h1>
    </div>
  );
}
