#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#include <ctime>
#include <algorithm>

#ifdef _WIN32
    #include <conio.h>
    #include <windows.h>
    #define GETCH() _getch()
    #define KB_HIT() _kbhit()
    void SleepMs(int ms) { Sleep(ms); }
#else
    #include <cstdio>
    #include <unistd.h>
    int GETCH() { return getchar(); }
    #define KB_HIT() 0
    void SleepMs(int ms) { usleep(ms * 1000); }
#endif

using namespace std;

const int GAME_HEIGHT = 20;
const int GAME_WIDTH  = 80;
const int MAX_HEALTH  = 5;
const int FRAME_DELAY_MS = 50;

struct Enemy {
    string word;
    int x;
    int y;
    int speed;
    int progress;
};

vector<string> word_list = {
    "gemini", "keyboard", "console", "terminal", "algorithm",
    "processor", "function", "variable", "include", "vector",
    "boolean", "integer", "string", "iterate", "compile",
    "defense", "shooter", "realtime", "typing", "project"
};

vector<Enemy> enemies;
string current_input = "";
int health = MAX_HEALTH;
int score = 0;
int frame_count = 0;
int active_target_index = -1;

void ClearScreen() {
#ifdef _WIN32
    system("cls");
#else
    cout << "\033[2J\033[1;1H";
#endif
}

string GetDisplayWord(const Enemy& enemy) {
    string display_word = "";
    for (int i = 0; i < enemy.progress; ++i) {
        display_word += "\033[32m" + string(1, enemy.word[i]) + "\033[0m";
    }
    display_word += enemy.word.substr(enemy.progress);
    return display_word;
}

void SpawnEnemy() {
    if (enemies.size() >= 10) return;

    string new_word = word_list[rand() % word_list.size()];
    int max_x = GAME_WIDTH - (int)new_word.length();
    if (max_x < 0) max_x = 0;

    Enemy new_enemy = {
        new_word,
        max_x > 0 ? rand() % max_x : 0,
        0,
        1,
        0
    };

    enemies.push_back(new_enemy);
}

void DrawGame() {
    ClearScreen();

    cout << "\033[1m=======================================\n";
    cout << " TYPING DEFENSE SHOOTER (Type to destroy)\n";
    cout << "=======================================\033[0m\n";

    cout << " Health: \033[31m";
    for (int i = 0; i < health; ++i) cout << "❤";
    cout << "\033[0m (" << health << "/" << MAX_HEALTH << ") ";

    cout << " Score: \033[33m" << score << "\033[0m\n";

    cout << "---------------------------------------\n";

    for (const auto& enemy : enemies) {
        if (enemy.y >= 0 && enemy.y < GAME_HEIGHT) {
            cout << "\033[s";
            cout << "\033[" << enemy.y + 7 << ";" << enemy.x + 1 << "H";

            bool is_active = (&enemy - &enemies[0] == active_target_index);
            string display_word = GetDisplayWord(enemy);

            if (is_active) cout << "\033[44m";
            cout << display_word << "\033[0m";
            cout << "\033[u";
        }
    }

    cout << "\033[s";
    cout << "\033[" << GAME_HEIGHT + 7 << ";1H";
    cout << "\033[41m\033[1m" << string(GAME_WIDTH, '=') << "\033[0m\n";
    cout << "Defense Line Reached! (Health Penalty)\n";
    cout << string(GAME_WIDTH, '-') << "\n";

    cout << "Type: > \033[36m" << current_input << "\033[0m";
    cout << string(GAME_WIDTH - current_input.length() - 7, ' ');

    cout.flush();
}

void HandleInput(char typed_char) {
    if (!isprint(typed_char) && typed_char != 8 && typed_char != 127) return;

    // Backspace
    if (typed_char == 8 || typed_char == 127) {
        if (!current_input.empty()) {
            current_input.pop_back();
            if (active_target_index != -1 &&
                enemies[active_target_index].progress > 0) {
                enemies[active_target_index].progress--;
            }
        }
        return;
    }

    current_input += typed_char;

    int old_active_index = active_target_index;
    active_target_index = -1;

    // Continue current enemy
    if (old_active_index != -1 && old_active_index < (int)enemies.size()) {
        Enemy& e = enemies[old_active_index];

        if (e.word.length() > e.progress &&
            typed_char == e.word[e.progress]) {

            e.progress++;
            active_target_index = old_active_index;

            if (e.progress == e.word.length()) {
                score += e.word.length();
                enemies.erase(enemies.begin() + old_active_index);
                current_input = "";
                active_target_index = -1;
                return;
            }
        } else {
            e.progress = 0;
        }
    }

    // Search new enemy
    if (active_target_index == -1) {
        for (size_t i = 0; i < enemies.size(); ++i) {
            if (enemies[i].word[0] == typed_char) {
                enemies[i].progress = 1;
                active_target_index = i;
                break;
            }
        }
        if (active_target_index != -1) {
            current_input = string(1, typed_char);
        }
    }
}

void UpdateGame() {
    frame_count++;

    if (frame_count % 10 == 0) {
        for (int i = 0; i < (int)enemies.size();) {
            enemies[i].y += enemies[i].speed;

            if (enemies[i].y >= GAME_HEIGHT) {
                health--;
                int removed_index = i;

                if (active_target_index == i) {
                    active_target_index = -1;
                    current_input = "";
                }

                enemies.erase(enemies.begin() + i);

                if (active_target_index > removed_index)
                    active_target_index--;

                if (health <= 0) return;

            } else {
                ++i;
            }
        }
    }

    int spawn_delay = 100 - min(score / 5, 80);
    if (frame_count % spawn_delay == 0) {
        SpawnEnemy();
    }
}

void InitializeGame() {
    srand(time(0));
    health = MAX_HEALTH;
    score = 0;
    frame_count = 0;
    enemies.clear();
    current_input = "";
    active_target_index = -1;

    SpawnEnemy();
    SpawnEnemy();
    SpawnEnemy();
}

void GameLoop() {
    InitializeGame();

    cout << "\033[?25l"; // hide cursor

    while (health > 0) {
#ifdef _WIN32
        if (KB_HIT()) {
            char typed_char = (char)GETCH();
            HandleInput(typed_char);
        }
#endif
        UpdateGame();
        DrawGame();
        SleepMs(FRAME_DELAY_MS);
    }

    ClearScreen();
    cout << "\033[1m=======================================\n";
    cout << "               GAME OVER\n";
    cout << "=======================================\033[0m\n";

    cout << "\nFinal Score: \033[33m" << score << "\033[0m\n";
    cout << "\nPress any key to exit...\n";

    (void)GETCH();
    cout << "\033[?25h";
}

int main() {
    GameLoop();
    return 0;
}
