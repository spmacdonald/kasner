#include <iostream>
#include <cmath>
#include <vector>
#include <algorithm>

unsigned long ipow(int x, int y);


bool is_periodic(const std::string& sequence)
{
    for (unsigned i = 0; i < sequence.size() - 1; i++) {
        if (sequence[i] == sequence[i + 1]) {
            return false;
        }
    }

    std::string::const_iterator it;

    it = find(sequence.begin(), sequence.end(), 0);
    if (it == sequence.end()) return false;
    it = find(sequence.begin(), sequence.end(), 1);
    if (it == sequence.end()) return false;
    it = find(sequence.begin(), sequence.end(), 2);
    if (it == sequence.end()) return false;

    return true;
}


int circular_min(const std::string& sequence)
{
    int i = 0;
    int j = 1;
    int k = 0;
    int m = sequence.size();

    std::string b(2*m+1, 0);
    b[0] = -1;

    while (k+j < 2*m) {
        if (j - i == m) {
            break;
        }
        b[j] = i;
        while (i >= 0 && sequence[(k+j) % m] != sequence[(k+i) % m]) {
            if (sequence[(k+j) % m] < sequence[(k+i) % m]) {
                k = k + j - i;
                j = i;
            }
            i = b[i];
        }
        i++;
        j++;
    }

    return k;
}


void next_sequence(std::string& sequence, size_t i=0)
{
    if (i == 0) {
        i = sequence.size() - 1;
    }

    sequence[i]++;

    if (sequence[i] > 2) {
        sequence[i] = 0;
        next_sequence(sequence, i - 1);
    }

    if (sequence[i - 1] == sequence[i]) {
        next_sequence(sequence, i);
    }
}


void count_number_periodic_paths(int n)
{
    std::string sequence(n, 0);

    for (unsigned i = 0; i < sequence.size(); i++) {
        sequence[i] = i % 2;
    }

    std::vector<std::string> unique_sequences;

    for (unsigned long long i = 1; i < ipow(2, (n - 1)); i++) {
        next_sequence(sequence);
        std::string least_conjugate(sequence);
        int k = circular_min(sequence);
        rotate(least_conjugate.begin(), least_conjugate.begin() + k, least_conjugate.end());
        if (is_periodic(least_conjugate) && !binary_search(unique_sequences.begin(), unique_sequences.end(), least_conjugate)) {
            unique_sequences.push_back(least_conjugate);
        }
    }

    std::cout << n << " " << unique_sequences.size() << std::endl;
}


unsigned long ipow(int x, int y) {
    return static_cast<unsigned long>(pow(static_cast<double>(x), static_cast<double>(y)));
}


int main()
{
    for (int i = 3; i <= 25; i++) {
        count_number_periodic_paths(i);
    }
}
