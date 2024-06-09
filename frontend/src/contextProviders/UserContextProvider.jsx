import { createContext, useState } from "react";

export default function UserContextProvider({ children }) {
  const UserContext = createContext(null);

  const [user, setUser] = useState(null); // TODO: load the user from localStorage

  return <UserContext.Provider value={{ user: user, setUser: setUser }}>{children}</UserContext.Provider>;
}
