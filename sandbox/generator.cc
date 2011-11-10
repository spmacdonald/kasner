#include <iostream>
#include <iterator>
#include <algorithm>
#include <vector>
#include <math.h>

using namespace std;

class Path
{
private:
    vector<int> sequence;
    void init();

public:
    Path() {}
    Path(int& n) : sequence(n) { init(); }
    int& operator[](const int& i) { return sequence[i]; }
    size_t size() const { return sequence.size(); }

    vector<int>::iterator begin() { return sequence.begin(); }
    vector<int>::iterator end() { return sequence.end(); }
    vector<int>::const_iterator begin() const { return sequence.begin(); }
    vector<int>::const_iterator end() const { return sequence.end(); }

    bool operator<(const Path& rhs) const;
    bool operator==(Path& rhs);

    friend ostream& operator<<(ostream& output, const Path& p);
};

void Path::init()
{
    for (size_t i = 0; i < sequence.size(); ++i)
    {
        sequence[i] = i % 2;
    }
}

bool Path::operator<(const Path& rhs) const
{
    return lexicographical_compare(
            (*this).begin(), (*this).end(), rhs.begin(), rhs.end());
}

bool Path::operator==(Path& rhs)
{
    for (size_t i = 0; i < rhs.size(); ++i)
    {
        if ((*this)[i] != rhs[i])
        {
            return false;
        }
    }

    return true;
}

ostream& operator<<(ostream& output, const Path& p)
{
    copy(p.sequence.begin(), p.sequence.end(), ostream_iterator<int>(cout));

    return output;
}

void nextpath(Path& p, int n)
{
    p[n]++;
    if (p[n] > 2)
    {
        p[n] = 0;
        nextpath(p, (n-1));
    }
    if (p[n-1] == p[n])
    {
        nextpath(p, n);
    }
}

int circularMin(Path& p)
{
    int i = 0;
    int j = 1;
    int k = 0;
    int m = p.size();

    vector<int> b(2 * m + 1, 0);
    b[0] = -1;

    while (k + j < 2 * m)
    {
        if (j - i == m)
            break;

        b[j] = i;
        while (i >= 0 && p[(k + j) % m] != p[(k + i) % m])
        {
            if (p[(k + j) % m] < p[(k + i) % m])
            {
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

bool isPathTerminating(Path& p)
{
    int zeroCount = 0;
    int oneCount = 0;
    int twoCount = 0;

    for (size_t i = 0; i < p.size(); ++i)
    {
        if (p[i] == 0)
        {
            zeroCount++;
        }
        else if (p[i] == 1)
        {
            oneCount++;
        }
        else if (p[i] == 2)
        {
            twoCount++;
        }
        else
        {
            cout << "Expected path value to be either 0,1,2." << endl;
            abort();
        }
    }

    if (zeroCount == 0 || oneCount == 0 || twoCount == 0)
    {
        return false;
    }

    return true;
}

bool isPathBalanced(Path& p)
{
    // Assumes path is rotated to its lexicographically least conjugate.
    for (size_t i = 0; i < p.size() - 1; ++i)
    {
        if (p[i] == p[i + 1])
        {
            return false;
        }
    }

    return true;
}

bool isPathValid(Path& p)
{
    return isPathTerminating(p) && isPathBalanced(p);
}

void removeInvalidPaths(vector<Path>& paths)
{
    vector<Path>::iterator pathIter;
    for (pathIter = paths.begin(); pathIter != paths.end(); )
    {
        if (!isPathValid(*pathIter))
        {
            pathIter = paths.erase(pathIter);
        }
        else
        {
            ++pathIter;
        }
    }
}

int main(int argc, char* argv[])
{
    int n(atoi(argv[1]));
    Path p = Path(n);

    // Populate vector with search space.
    vector<Path> paths(pow(2, n-1), Path(n));
    for (int i = 0; i < pow(2, n-1); ++i)
    {
        paths[i] = p;
        nextpath(p, n-1);
    }
    // cout << "Total search space: " << paths.size() << endl;

    // Rotate all paths to their least conjugate order.
    for (size_t i = 0; i < paths.size(); ++i) {
        int k = circularMin(paths[i]);
        rotate(paths[i].begin(), paths[i].begin()+k, paths[i].end());
    }

    // Sort the paths in the search space.
    sort(paths.begin(), paths.end());

    // Remove duplicates.
    vector<Path>::iterator i = unique(paths.begin(), paths.end());
    paths.resize(i - paths.begin());
    // cout << "Number of paths remaining after duplicate paths removed: " << paths.size() << endl;

    // Remove paths that do not contain at least one occurance of each letter.
    removeInvalidPaths(paths);
    cout << "Number of paths: " << paths.size() << endl;

    // Output the path strings.
    for (size_t i = 0; i < paths.size(); ++i)
    {
        cout << paths[i] << endl;
    }


    return 0;
}
