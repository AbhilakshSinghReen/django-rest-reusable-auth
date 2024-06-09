function isPathnameIncluded(checkerPathnames, targetPathname) {
  for (const pathname of checkerPathnames) {
    if (targetPathname.startsWith(pathname)) {
      return true;
    }
  }

  return false;
}

export { isPathnameIncluded };
