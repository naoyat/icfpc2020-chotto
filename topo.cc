

#include <bits/stdc++.h>
using namespace std;
#include "cout11.h"

#define NDEBUG
#ifdef DEBUG
#undef NDEBUG
#endif
#include <cassert>

#ifdef DEBUG
#define debug(...) fprintf(stderr, __VA_ARGS__)
#else
#define debug(...)
#endif

typedef long long ll;
typedef long double Double;
typedef unsigned long long ull;
typedef pair<int, int> ii;
typedef pair<ll, ll> llll;
typedef pair<double, double> dd;

typedef vector<int> vi;
typedef vector<vector<int>> vvi;
typedef vector<ii> vii;
typedef vector<vector<ii>> vvii;
typedef vector<ll> vll;
typedef vector<vector<ll>> vvll;
typedef vector<llll> vllll;
typedef vector<bool> vb;
typedef vector<string> vs;
typedef vector<double> vd;
typedef vector<long double> vD;

#define sz(a) int((a).size())
#define pb push_back
#define eb emplace_back
#define FOR(var, from, to) for (int var = (from); var <= (to); ++var)
#define rep(var, n) for (int var = 0; var < (n); ++var)
#define rep1(var, n) for (int var = 1; var <= (n); ++var)
#define repC2(vari, varj, n)               \
  for (int vari = 0; vari < (n)-1; ++vari) \
    for (int varj = vari + 1; varj < (n); ++varj)
#define repC3(vari, varj, vark, n)                  \
  for (int vari = 0; vari < (n)-2; ++vari)          \
    for (int varj = vari + 1; varj < (n)-1; ++varj) \
      for (int vark = varj + 1; vark < (n); ++vark)
#define ALL(c) (c).begin(), (c).end()
#define RALL(c) (c).rbegin(), (c).rend()
#define tr(i, c) for (auto i = (c).begin(); i != (c).end(); ++i)
#define found(s, e) ((s).find(e) != (s).end())
#define mset(arr, val) memset(arr, val, sizeof(arr))
#define mid(x, y) ((x) + ((y) - (x)) / 2)
#define IN(x, a, b) ((a) <= (x) && (x) <= (b))
#define cons make_pair
#define clamp(v, lo, hi) min(max(v, lo), hi)
#define ABS(x) max((x), -(x))
#define PQ(T) priority_queue<T, vector<T>, greater<T>>

template <typename T1, typename T2>
inline void amin(T1& a, T2 const& b) {
  if (a > b) a = b;
}
template <typename T1, typename T2>
inline void amax(T1& a, T2 const& b) {
  if (a < b) a = b;
}
template <typename X, typename T>
auto vectors(X x, T a) {
  return vector<T>(x, a);
}
template <typename X, typename Y, typename Z, typename... Zs>
auto vectors(X x, Y y, Z z, Zs... zs) {
  auto cont = vectors(y, z, zs...);
  return vector<decltype(cont)>(x, cont);
}

inline ll square(ll x) { return x * x; }
inline ll gcd(ll a, ll b) {
  while (a) swap(a, b %= a);
  return b;
}
inline ll lcm(ll a, ll b) { return a / gcd(a, b) * b; }
template <typename T>
inline T mod(T a, T b) {
  return ((a % b) + b) % b;
}

template <typename T>
int find_left(vector<T>& v, T elem) {
  // elemそのものがあればそのindexを、なければ１つ下（左）のindexを返す
  return (int)(upper_bound(v.begin(), v.end(), elem) - v.begin()) - 1;
}
template <typename T>
int find_right(vector<T>& v, T elem) {
  // elemそのものがあればそのindexを、なければ１つ上（右）のindexを返す
  return (int)(lower_bound(v.begin(), v.end(), elem) - v.begin());
}

const ll MOD = 1000000007LL;

inline ll ADD(ll x, ll y) { return (x + y) % MOD; }
inline ll SUB(ll x, ll y) { return (x - y + MOD) % MOD; }
inline ll MUL(ll x, ll y) { return x * y % MOD; }
inline ll POW(ll x, ll e) {
  ll v = 1;
  for (; e; x = MUL(x, x), e >>= 1)
    if (e & 1) v = MUL(v, x);
  return v;
}
inline ll INV(ll y) { /*assert(y%MOD!=0);*/
  return POW(y, MOD - 2);
}
inline ll DIV(ll x, ll y) { return MUL(x, INV(y)); }
// ll comb(ll n, ll k) { ll v=1; for(ll i=1; i<=k; i++) v = DIV(MUL(v, n-i+1),i); return v; }
//

void horizontal(vector<int>& v) {
  int L = v.size();
  for (int i = 0; i < L; ++i) {
    printf("%d%c", v[i], (i == L - 1) ? '\n' : ' ');
  }
}
void horizontall(vector<long long>& v) {
  int L = v.size();
  for (int i = 0; i < L; ++i) {
    printf("%lld%c", v[i], (i == L - 1) ? '\n' : ' ');
  }
}
string concat(vector<string>& strs) {
  stringstream ss;
  tr(it, strs) ss << *it;
  return ss.str();
}

vector<string> split(string str, int delim = ' ') {
  vector<string> result;

  const char* s = str.c_str();
  if (delim == ' ') {
    for (const char* p = s; *p; p++) {
      if (*p == delim)
        s++;
      else
        break;
    }
    if (!*s) return result;

    for (const char* p = s; *p; p++) {
      if (*p == delim) {
        if (s < p) {
          string a(s, p - s);
          result.push_back(a);
        }
        s = p + 1;
      }
    }
    if (*s) result.push_back(s);
  } else {
    for (const char* p = s; *p; p++) {
      if (*p == delim) {
        string a(s, p - s);
        result.push_back(a);
        s = p + 1;
        if (*s == '\0') result.push_back("");
      }
    }
    if (*s) result.push_back(s);
  }

  return result;
}

vector<int> map_atoi(vector<string> nums) {
  vector<int> vals(nums.size());
  for (int i = nums.size() - 1; i >= 0; i--) vals[i] = atoi(nums[i].c_str());
  return vals;
}

template <typename T>
vector<T> toposort(const set<T> group, const set<pair<T, T>>& arcs) {
  map<T, set<T>> from, to;
  for (pair<T, T> arc : arcs) {
    T u = arc.first, v = arc.second;
    from[u].insert(v);
    to[v].insert(u);
  }
  int E = arcs.size();

  set<T> S;
  for (T i : group) {
    if (!found(to, i)) S.insert(i);
  }

  vector<T> L;
  while (!S.empty()) {
    T u = *S.begin();
    S.erase(u);
    L.push_back(u);
    for (T v : from[u]) {
      to[v].erase(u);
      --E;
      if (to[v].empty()) {
        S.insert(v);
      }
    }
  }

  if (E != 0) {
    return vector<T>{};
  }

  return L;
}

int main() {
  map<string, vs> dep;
  set<string> s_token;
  set<pair<string, string>> arcs;

  string line;
  while (!cin.eof()) {
    getline(cin, line);
    vs tokens = split(line, ' ');
    if (tokens.empty()) break;
    for (string& token : tokens) {
      s_token.insert(token);
    }
    string head = tokens[0];

    // dep[head] = vs(tokens.begin() + 2, tokens.end());
    for (int i = 2; i < tokens.size(); ++i) {
      if (tokens[i] == head) continue;
      arcs.emplace(head, tokens[i]);
    }
    // cout << head << " : " << dep[head] << endl;
  }
  vector<string> ord = toposort<string>(s_token, arcs);
  cout << ord << endl;

  //   int S = s_token.size();
  //   map<string, int> token_to_id;
  //   vector<string> id_to_token;
  //   int token_id = 0;
  //   for (const string& token : s_token) {
  //     if (token == "=") continue;
  //     id_to_token.pb(token);
  //     token_to_id[token] = token_id++;
  //   }

  //   map<int, vi> depi;
  //   for (auto& p : dep) {
  //     int head_id = token_to_id[p.first];
  //     for (string& t : p.second) {
  //       depi[head_id].pb(token_to_id[t]);
  //     }
  //     cout << head_id << " : " << depi[head_id] << endl;
  //   }
  //   printf("// galaxy = %d\n", token_to_id["galaxy"]);

  // printf("// 392 = %s\n", id_to_token[392].c_str());

  //   vector<T> toposort(const set<T> group, const set<pair<T, T>>& arcs)
  return 0;
}
