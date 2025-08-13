// Create a user with readWrite role for the 'mydatabase' database
db.createUser({
  user: "test",
  pwd: "test",
  roles: [
    { role: "readWrite", db: "users" }
  ]
});

// Switch to your database
db = db.getSiblingDB('users');

// Create a collection named 'myCollection'
db.createCollection('myCollection');

