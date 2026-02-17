export function getUsers() {
  const data = localStorage.getItem("users");
  return data ? JSON.parse(data) : [];
}

export function saveUsers(users) {
  localStorage.setItem("users", JSON.stringify(users));
}

export function getGroups() {
  const data = localStorage.getItem("groups");
  return data ? JSON.parse(data) : [];
}

export function saveGroups(groups) {
  localStorage.setItem("groups", JSON.stringify(groups));
}
