// JavaScript ES6 Sample
class User {
    constructor(name, email) {
        this.name = name;
        this.email = email;
        this.loginCount = 0;
    }

    login() {
        this.loginCount++;
        console.log(`${this.name} logged in. Total logins: ${this.loginCount}`);
    }

    updateEmail(newEmail) {
        this.email = newEmail;
        console.log(`Email updated to: ${newEmail}`);
    }

    getInfo() {
        return {
            name: this.name,
            email: this.email,
            logins: this.loginCount
        };
    }
}

function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function createUser(name, email) {
    if (!validateEmail(email)) {
        throw new Error('Invalid email address');
    }
    return new User(name, email);
}

// Usage
const user = createUser('John Doe', 'john@example.com');
user.login();
user.login();
console.log(user.getInfo());
