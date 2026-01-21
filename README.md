# PyShell - Python Based CLI 
### (initiative by @ansh.mn.soni)

## 👉 Introduction:
PyShell is a custom-built command-line interface (CLI) that serves as a lightweight yet powerful terminal, developed using Python. It allows users to interact with their system, manage files, process system commands, and perform various utility functions. With a focus on simplicity, speed, and usability, PyShell enhances the standard terminal experience by integrating automation, process management, and network utilities.

## 🔑 Key Advantages:

#### 1️⃣ Task Scheduling
###### Preview </br></br>
![image](https://github.com/user-attachments/assets/d0cf8b40-52ca-47a4-a60c-26278e65bc69)

#### 2️⃣ Weather Tracking
###### Preview </br></br>
![image](https://github.com/user-attachments/assets/953cbd34-397b-45be-a274-4e0d2e584c4b)

#### 3️⃣ in-built Calculator
###### Preview </br></br>
![image](https://github.com/user-attachments/assets/f65045b0-9e4c-43e8-a46c-403344480542)

#### 4️⃣ Automate Password Generator
###### Preview </br></br>
![image](https://github.com/user-attachments/assets/0ad4ac81-66dc-495f-a897-2cb27f3997e0)

#### 5️⃣ Supports all basic linux commands
- `ls`
- `ls -all`
- `mkdir`
- `touch`
- `rm`
- `sysinfo`
- `network` etc...

#### 6️⃣ Supports synchronization
- `list process`
- `kill process`
- `force stop`
- `renaming file` in between the program

#### 7️⃣ Simple and Clean Terminal
###### Preview </br></br>
![Screenshot 2025-05-18 125323](https://github.com/user-attachments/assets/55692d28-4f35-4236-b9ac-c976e85d5891)

#### 8️⃣ Play Song right through terminal
###### Preview </br></br>
![Screenshot 2025-05-18 132600](https://github.com/user-attachments/assets/d254ab8b-da7f-4d78-b5c3-45233a9ffd96)

![Screenshot 2025-05-18 132534](https://github.com/user-attachments/assets/f1c38833-bed4-47ab-8b20-ce046474c1e0)

#### 9️⃣ Change terminal Functionality
###### Preview </br></br>
![Screenshot 2025-05-18 130106](https://github.com/user-attachments/assets/da67e659-b3ec-4a57-9cf9-a25558248b9c)

![Screenshot 2025-05-18 130126](https://github.com/user-attachments/assets/84487e3f-4d4e-43e2-9172-9bf1490dbdaf)

![Screenshot 2025-05-18 130147](https://github.com/user-attachments/assets/94dd78a3-b3e7-467e-9aa2-a480c494d053)

![Screenshot 2025-05-18 130201](https://github.com/user-attachments/assets/d59e18b1-c88b-44cf-badb-7eabd787aff7)

![Screenshot 2025-05-18 130227](https://github.com/user-attachments/assets/2fd1dda3-8e27-4ffc-b3a5-44dcd04765b3)

![Screenshot 2025-05-18 130301](https://github.com/user-attachments/assets/9fba52c3-b1a2-417e-9180-a5a1935cbb33)

#### 🔟 Calculus Operations in Calculator
###### Preview </br></br>
![Screenshot 2025-05-18 131128](https://github.com/user-attachments/assets/964a179f-0cf6-457a-b12e-b3c9021f9bf0)

![Screenshot 2025-05-18 131248](https://github.com/user-attachments/assets/2f6dcd75-5a90-4f9f-802b-b36fbbe6a25e)

![Screenshot 2025-05-18 131424](https://github.com/user-attachments/assets/a34d24c1-1a6b-4be2-88b8-1d1abd43f801)

#### 1️⃣1️⃣ Stock Monitoring
###### Preview </br> </br>
<img width="1447" height="543" alt="image" src="https://github.com/user-attachments/assets/c4a7ebc3-1d6e-433a-b0f5-296167138684" />

#### 1️⃣2️⃣ Short Prompt Feature
###### Preview </br> </br>
<img width="1415" height="389" alt="image" src="https://github.com/user-attachments/assets/68fc20b2-4f3a-405d-9745-17a6f209206c" />

<img width="1426" height="331" alt="image" src="https://github.com/user-attachments/assets/d010b20e-4298-40db-9f45-82b9183c85ca" />


#### and many more...

## 🧑‍💻 How to setup:
1️⃣ Clone the Repository:</br>
```sh
pip install pyshellcli
```

2️⃣ Install all require dependencies:</br>
```sh
pip install -r requirements.txt
```
###### Now, you are good to go...

## How to use:
1️⃣ To experience "pyshell" run:</br>
```sh
from pyshell.main import main

main()
```

2️⃣ Run individual module:</br>
1. Equation Solver:
```sh
from pyshellcli.equations import Equations

Equations().solve_equation(["x + y = 3; x - y = 3"])
```

2. Playing Song:
```sh
from pyshellcli.song import Song

Song().play_song("Janam Janam")
```

3. Plotting Graphs:
```sh
from pyshellcli.graphs import GraphPlotter

GraphPlotter().plot_implicit()
```

4. Check Weather:
```sh
from pyshellcli.weather import Weather

Weather().get_weather(["Navsari"])
```

5. Check Stock:
```sh
from pyshellcli.stocks import Stock

Stock().get_stock_info(["IBM"])
```

6. Play Games:
```sh
from pyshellcli.game import Game

Game().play_game()
```

and many more...

## 🤝 Contributing to PyShell

Thank you for considering contributing! Please follow these steps:

1. **Fork** the repository.
2. **Create a new branch** (`git checkout -b feature-branch`).
3. **Commit your changes** (`git commit -m "Add new feature"`).
4. **Push to your fork** (`git push origin feature-branch`).
5. **Submit a Pull Request** and wait for review.

# 📢 Connect with Me
If you found this project helpful or have any suggestions, feel free to connect:

- [![LinkedIn](https://img.shields.io/badge/LinkedIn-anshmnsoni-0077B5.svg?logo=linkedin)](https://www.linkedin.com/in/anshmnsoni)  
- [![GitHub](https://img.shields.io/badge/GitHub-AnshMNSoni-181717.svg?logo=github)](https://github.com/AnshMNSoni)
- [![Reddit](https://img.shields.io/badge/Reddit-u/AnshMNSoni-FF4500.svg?logo=reddit)](https://www.reddit.com/user/AnshMNSoni)

## Thankyou 💫
