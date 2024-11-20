function Person(firstName, lastName, middleName) {
    this._firstName = firstName;
    this._lastName = lastName;
    this._middleName = middleName;
}


Object.defineProperty(Person.prototype, 'firstName', {
    get: function() {
        return this._firstName;
    },
    set: function(value) {
        this._firstName = value;
    }
});

Object.defineProperty(Person.prototype, 'lastName', {
    get: function() {
        return this._lastName;
    },
    set: function(value) {
        this._lastName = value;
    }
});

Object.defineProperty(Person.prototype, 'middleName', {
    get: function() {
        return this._middleName;
    },
    set: function(value) {
        this._middleName = value;
    }
});


Person.prototype.getFullName = function() {
    return `${this._lastName} ${this._firstName} ${this._middleName}`;
};

Person.prototype.isComplete = function() {
    return !!(this._firstName && this._lastName && this._middleName);
};


function BankClient(firstName, lastName, middleName) {
    Person.call(this, firstName, lastName, middleName);
    this.accounts = [];
}

BankClient.prototype = Object.create(Person.prototype);
BankClient.prototype.constructor = BankClient;

BankClient.clients = [];

console.log(BankClient.prototype);


BankClient.prototype.addAccount = function(accountNumber, deposit) {
    const existingAccount = this.accounts.find(acc => acc.accountNumber === accountNumber);
    if (existingAccount) {
        existingAccount.deposit += deposit;
    } else {
        this.accounts.push({ accountNumber, deposit });
    }
};

BankClient.prototype.totalDeposit = function() {
    return this.accounts.reduce((total, account) => total + account.deposit, 0);
};

BankClient.prototype.hasMultipleAccounts = function() {
    return this.accounts.length > 1;
};

BankClient.prototype.displayAccounts = function() {
    return this.accounts.map(acc => `(счет: ${acc.accountNumber}, вклад: ${acc.deposit}$)`).join(', ');
};

BankClient.prototype.displayResult = function() {
    return `${this.getFullName()} имеет счета: ${this.displayAccounts() === '' ? '(нет счетов)' : this.displayAccounts()}; Общая сумма вкладов: ${this.totalDeposit()}$`;
};


BankClient.addClientFromForm = function(event) {
    event.preventDefault();

    const form = event.target;
    const firstName = form.firstName.value.trim();
    const lastName = form.lastName.value.trim();
    const middleName = form.middleName.value.trim();

    if (!firstName || !lastName || !middleName) {
        document.querySelector('#error-message-client').textContent = 'Пожалуйста, заполните все обязательные поля (Имя, Фамилия, Отчество).';
        return;
    }

    const newClient = new BankClient(firstName, lastName, middleName);
    BankClient.clients.push(newClient);

    form.reset();
    document.querySelector('#error-message-client').textContent = '';

    BankClient.updateClientSelect(document.querySelector('#client-select'));
    BankClient.updateClientList(document.querySelector('#client-list'));
    BankClient.updateResultList(document.querySelector('#result-list'));
};

BankClient.addAccountToClient = function(event) {
    event.preventDefault();

    const form = event.target;

    if (isNaN(+form.accountNumber.value) || form.accountNumber.value.trim() === '') {
        document.querySelector('#error-message-account').textContent = 'Пожалуйста, укажите номер счета как целое положительное число.';
        return;
    }

    const accountNumber = parseInt(form.accountNumber.value.trim(), 10);
    const deposit = parseFloat(form.deposit.value);
    const clientName = form.clientName.value;

    if (!clientName) {
        document.querySelector('#error-message-account').textContent = 'Пожалуйста, выберите клиента.';
        return;
    }

    if (!accountNumber) {
        document.querySelector('#error-message-account').textContent = 'Пожалуйста, укажите номер счета как целое положительное число.';
        return;
    }

    if (!Number.isInteger(accountNumber) || accountNumber <= 0) {
        document.querySelector('#error-message-account').textContent = 'Номер счета должен быть целым положительным числом.';
        return;
    }

    if (isNaN(deposit) || deposit <= 0) {
        document.querySelector('#error-message-account').textContent = 'Пожалуйста, укажите положительную сумму вклада.';
        return;
    }

    const client = BankClient.clients.find(c => c.getFullName() === clientName);
    if (client) {
        client.addAccount(accountNumber, deposit);
    } else {
        document.querySelector('#error-message-account').textContent = 'Клиент не найден.';
        return;
    }

    form.reset();
    document.querySelector('#error-message-account').textContent = '';

    BankClient.updateClientList(document.querySelector('#client-list'));
    BankClient.updateResultList(document.querySelector('#result-list'));
};

BankClient.updateClientSelect = function(clientSelect) {
    clientSelect.innerHTML = '';

    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = '--Выберите клиента--';
    defaultOption.selected = true;
    defaultOption.disabled = true;
    defaultOption.hidden = true;
    clientSelect.appendChild(defaultOption);

    BankClient.clients.forEach(client => {
        const option = document.createElement('option');
        option.value = client.getFullName();
        option.textContent = client.getFullName();
        clientSelect.appendChild(option);
    });
};

BankClient.updateResultList = function(resultList) {
    resultList.innerHTML = '';

    const multiAccountClients = BankClient.findClientsWithMultipleAccounts();
    multiAccountClients.forEach(client => {
        const resultDiv = document.createElement('div');
        resultDiv.textContent = `${client.getFullName()} имеет в депозите ${client.totalDeposit()}$`;
        resultList.appendChild(resultDiv);
    });
};

BankClient.updateClientList = function(clientList) {
    clientList.innerHTML = '';

    BankClient.clients.forEach(client => {
        const clientDiv = document.createElement('div');
        clientDiv.textContent = client.displayResult();
        clientList.appendChild(clientDiv);
    });
};

BankClient.findClientsWithMultipleAccounts = function() {
    return BankClient.clients.filter(client => client.hasMultipleAccounts());
};


document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#client-form').addEventListener('submit', BankClient.addClientFromForm);
    document.querySelector('#account-form').addEventListener('submit', BankClient.addAccountToClient);
});