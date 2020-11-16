




































/*
========================================================================================
Determinant |A| & Inverse A^-1 = adjoint(A) i.e cofactor matrix transposed / determinant
=========================================================================================

#include<bits/stdc++.h>
using namespace std;
// temp matrix removing the pth row and qth col (cofactor matrix)
void cofactors(int m[10][10],int temp[10][10],int p,int q,int n)
{
    int row=0,col=0;
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<n;j++)
        {
            if(i!=p && j!=q)
                temp[row][col++]=m[i][j];
            if(col==n-1)
            {
                col=0;
                row++;
            }
        }
    }
}

int det(int m[10][10],int n)
{
    if(n==1)
        return m[n-1][n-1];
    int ans=0;
    int sign=1;
    int temp[10][10];
    for(int i=0;i<n;i++)
    {
        cofactors(m,temp,0,i,n);
        ans+=sign*m[0][i]*det(temp,n-1); // recursive call to n-1 cofactor matrix
        sign=-sign;
    }
    return ans;
}

int main()
{
    int n;
    cout<<"rows for m"<<endl;
    cin>>n;
    int m[10][10];
    cout<<"Enter the elements of matrix"<<endl;
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<n;j++)
            cin>>m[i][j];
    }
    cout<<det(m,n);
    return 0;
}



*/


















/*
//Matrix Multiplication

#include<bits/stdc++.h>
using namespace std;
int main()
{
    int m,n,a,b,c,d;
    cout<<"rows and columns for m1"<<endl;
    cin>>m>>n;
    int m1[m][n];
    cout<<"rows and columns for m2"<<endl;
    cin>>a>>b;
    int m2[a][b];
    int m3[m][b];
    cout<<"Enter the elements of m1"<<endl;
    for(int i=0;i<m;i++)
    {
        for(int j=0;j<n;j++)
            cin>>m1[i][j];
    }
    cout<<"Enter the elements of m2"<<endl;
    for(int i=0;i<a;i++)
    {
        for(int j=0;j<b;j++)
            cin>>m2[i][j];
    }
    // main concept M1M2 (multiplied matrix contains sum of all the elements of row i mul by all the elements of column j)
    for(int i=0;i<m;i++)
    {
        for(int j=0;j<b;j++)
        {
            int sum=0;
            for(int k=0;k<n;k++)
                sum+=m1[i][k]*m2[k][j];
            m3[i][j]=sum;
        }
    }
    for(int i=0;i<m;i++)
    {
        for(int j=0;j<b;j++)
            cout<<m3[i][j]<<" ";
        cout<<endl;
    }

    return 0;
}

*/

















/*
===============================================================
Try some number theory
===============================================================
*/






























/*
=========================================================
Lowest Common Ancestor
=========================================================



#include<bits/stdc++.h>
using namespace std;
int sparse[20][20],n,node;
unordered_map<int,int> um;
vector<int> euler_tour,height;
void build_sparse(vector<int> a)     // sparse DS for range minimum in O(1)
{
    for(int i=0;i<n;i++)
        sparse[i][0]=i;

    for(int j=1;(1<<j)<=n;j++)        // sparse[i][j] store the minimum for [i..... 2^j-1]  (pow 2 windows)
    {
        for(int i=0;i+(1<<j)-1<n;i++)
        {
            if(a[sparse[i][j-1]]<=a[sparse[i+(1<<j-1)][j-1]])         // can break down kth pow of 2 to k-1 th power
                sparse[i][j]=sparse[i][j-1];
            else
                sparse[i][j]=sparse[i+(1<<j-1)][j-1];
        }
    }
}

int min_query(int l,int r)        // returns the minimum index in the range
{
    int j=(int)log2(r-l+1);
    if(sparse[l][j]<=sparse[r-(1<<j)+1][j])
        return sparse[l][j];
    else
        return sparse[r-(1<<j)+1][j];
}

void dfs(int n,int prev,int depth,vector<int> v[])
{
    euler_tour.push_back(n);
    height.push_back(depth);
    um[n]=euler_tour.size()-1;
    for(int i:v[n])
    {
        if(i!=prev)
        {
            dfs(i,n,depth+1,v);
            euler_tour.push_back(n);
            height.push_back(depth);
        }
    }
}

int main()
{
    int edges,a,b;
    cout<<"Enter nodes and edges"<<endl;
    cin>>node>>edges;
    vector<int> v[node+1];
    cout<<"enter edges"<<endl;
    for(int i=0;i<edges;i++)
    {
        cin>>a>>b;
        v[a].push_back(b);
        v[b].push_back(a);
    }
    dfs(1,0,1,v);
    n=height.size();
    build_sparse(height);
    int l=um[5];
    int r=um[7];
    if(r<l)
        swap(l,r);
    cout<<euler_tour[min_query(l,r)]<<endl;
    return 0;
}


/*

1 2
1 3
1 4
2 5
2 6
4 7
6 8

*/























































/*
=======================================================================
Subtree queries (update the value of a node,find the sum in a subtree)
=======================================================================

//Tree traversal can make a array in which trees are sequential with first element as root and rest can be calculated by getting the
size of the tree then it is a contiguous sequence from the root.

#include<bits/stdc++.h>
using namespace std;
vector<int> tree_trav;
unordered_map<int,int> um;         // for hashing the place of the node in traversal of the tree
int sz[10],val_tp[10],val[10];    // calculate size of subtree(for getting the range), val array for making fenwick tree or segment tree from that
int fenwick[10],node;
void traverse(int n,int prev,vector<int> v[])       // tree_trav,calculates size, assigns value to node,hash the place of node in tree_trav
{
    tree_trav.push_back(n);
    um[n]=tree_trav.size()-1;
    val[tree_trav.size()-1]=val_tp[n];
    sz[n]=1;
    for(int i:v[n])
    {
        if(i!=prev)
        {
            traverse(i,n,v);
            sz[n]+=sz[i];
        }
    }
}

//fenwick

void build(int x,int val)
{
    for(int i=x;i<=node;i+=(i & -i))
        fenwick[i]+=val;
}

int query(int x)
{
    int sum=0;
    for(int i=x;i>=1;i-=(i & -i))
        sum+=fenwick[i];
    return sum;
}

void update(int x,int p_val,int n_val)
{
    for(int i=x;i<=node;i+=(i & -i))
    {
        fenwick[i]-=p_val;
        fenwick[i]+=n_val;
    }
}

int main()
{
    int edges,a,b;
    cout<<"Enter nodes and edges"<<endl;
    cin>>node>>edges;
    vector<int> v[node+1];
    cout<<"enter edges"<<endl;
    for(int i=0;i<edges;i++)
    {
        cin>>a>>b;
        v[a].push_back(b);
        v[b].push_back(a);
    }
    cout<<"enter the value of nodes"<<endl;
    for(int i=1;i<=node;i++)
    {
        cin>>a;
        val_tp[i]=a;
    }
    tree_trav.push_back(0);
    traverse(1,0,v);
    for(int i=1;i<=node;i++)
        build(i,val[i]);
    int new_val=5;
    update(um[4],val[um[4]],new_val);   //updating prev 3 val of 4 to 5
    cout<<query(um[1]+sz[1]-1)-query(um[1]-1);
}



/*
1 2
1 3
1 4
1 5
2 6
4 7
4 8
4 9
2 3 5 3 1 4 4 3 1

1 2
1 3
1 4
1 5
2 6
4 7
4 8
4 9
enter the value of nodes
2 3 5 3 1 4 4 3 1
*/












































/*
=============================================================
finding the kth ancestor of a node in tree
=============================================================

#include<bits/stdc++.h>
using namespace std;
int anc[8+1][8+1];   //[nodes+1][k<=nodes+1]  where k is power of 2 (as tree can also have a single long chain)
void traverse(int n,int prev,vector<int> v[])
{
    for(int i:v[n])
    {
        if(i==prev)
            anc[n][1]=prev;
        else
            traverse(i,n,v);
    }
}

int main()
{
    int node,edges,a,b;
    cout<<"Enter nodes and edges"<<endl;
    cin>>node>>edges;
    vector<int> v[node+1];
    cout<<"enter edges"<<endl;
    for(int i=0;i<edges;i++)
    {
        cin>>a>>b;
        v[a].push_back(b);
        v[b].push_back(a);
    }
    anc[1][1]=0;anc[0][1]=0;
    traverse(1,0,v);   // calculate base case k=1(one ancestor)
    for(int q=2;q<=node;q=q*2)   // recursively calculate for all the powers  of 2 less than equal the nodes
    {
        for(int i=1;i<=node;i++)
            anc[i][q]=anc[anc[i][q/2]][q/2];
    }
    cout<<"enter the node and kth ancestor you want of that node (n,k)"<<endl;
    cin>>a>>b;
    for(int i=0;i<=16;i++)   // number of bits
    {
        if(b & (1<<i))
            a=anc[a][1<<i];
    }
    cout<<a<<endl;
    return 0;
}

/*

1 2
1 4
1 5
2 6
4 3
4 7
7 8

*/




































/*
=========================================================
Strongly connected components (kosaraju algorithm)
=========================================================


#include<bits/stdc++.h>
using namespace std;
stack<int> fintime_revdfs;

void dfs(int s,vector<int> v[],int vis[])
{
    if(vis[s]==1)
        return;
    vis[s]=1;
    for(int i:v[s])
        dfs(i,v,vis);
    fintime_revdfs.push(s);
}
void dfs_printer(int s,vector<int> v[],int vis[])
{
    if(vis[s]==1)
        return;
    vis[s]=1;
    cout<<s<<" ";
    for(int i:v[s])
        dfs_printer(i,v,vis);
}
int main()
{
    int node,edges,a,b;
    cout<<"Enter nodes and edges"<<endl;
    cin>>node>>edges;
    vector<int> v[node+1];
    int vis[node+1];
    cout<<"enter edges"<<endl;
    for(int i=0;i<edges;i++)
    {
        cin>>a>>b;
        v[a].push_back(b);
    }
    int flag=0,source=1;
    for(int i=1;i<=node;i++)
        vis[i]=0;
    while(flag==0)
    {
        dfs(source,v,vis);
        flag=1;
        for(int i=1;i<=node;i++)
        {
            if(vis[i]==0)
            {
                source=i;
                flag=0;
                break;
            }
        }
    }

    for(int i=1;i<=node;i++)
        vis[i]=0;
    vector<pair<int,int>> egg;
    for(int i=1;i<=node;i++)
    {
        for(int j:v[i])
            egg.push_back(make_pair(j,i));
    }
    vector<int> v_t[node+1];
    for(auto it:egg)
        v_t[it.first].push_back(it.second);
    for(int i=1;i<=node;i++)
        vis[i]=0;

    cout<<endl;
    while(!fintime_revdfs.empty())
    {
        int src=fintime_revdfs.top();
        fintime_revdfs.pop();
        if(vis[src]==1)
            continue;
        dfs_printer(src,v_t,vis);
        cout<<endl;
    }

    return 0;
}


/*
1 2
1 4
2 1
2 5
3 2
3 7
5 4
6 5
6 3
7 6
*/








































/*
==========================================================================
No of Paths from one node to all other nodes in an acyclic directed graph
==========================================================================


#include<bits/stdc++.h>
using namespace std;
vector<int> dfstopo;
void dfs(int s,vector<int> v[],int vis[])
{
    if(vis[s]==1)
        return;
    vis[s]=1;
    for(int i:v[s])
        dfs(i,v,vis);
    dfstopo.push_back(s);
}

int main()
{
    int node,edges,a,b;
    cout<<"Enter nodes and edges"<<endl;
    cin>>node>>edges;
    vector<int> v[node+1];
    int path[node+1],vis[node+1];
    cout<<"enter edges"<<endl;
    for(int i=0;i<edges;i++)
    {
        cin>>a>>b;
        v[a].push_back(b);
    }
    dfstopo.clear();
    for(int i=1;i<=node;i++)
        path[i]=0;
    path[1]=1;

    dfs(1,v,vis);
    reverse(dfstopo.begin(),dfstopo.end());
    for(int i:dfstopo)
    {
        for(int j:v[i])
            path[j]+=path[i];
    }
    for(int i=1;i<=node;i++)
        cout<<path[i]<<" ";
    cout<<endl;
    return 0;
}





/*
1 2
1 4
2 3
4 5
5 2
5 3
3 6
*/






































/*
========================================
Minimum spanning tree (Kruskals Algo)
========================================


#include<bits/stdc++.h>
using namespace std;

int finder(int link[],int x)
{
    while(x!=link[x])
        x=link[x];
    return x;
}

void join(int a,int b,int link[],int sz[])
{
    int par_a=finder(link,a);
    int par_b=finder(link,b);
    if(sz[par_a]>sz[par_b])
        swap(a,b);
    link[par_a]=par_b;
    sz[par_b]+=sz[par_a];
}

int main()
{
    int node,edge,final_weight=0;
    cout<<"Enter nodes and edges"<<endl;
    cin>>node>>edge;
    vector<tuple<int,int,int>> v;
    vector<pair<int,int>> final_tree;
    cout<<"Enter edges with weight"<<endl;
    int a,b,w;
    for(int i=0;i<edge;i++)
    {
        cin>>a>>b>>w;
        v.push_back(make_tuple(w,a,b));
        v.push_back(make_tuple(w,b,a));
    }
    sort(v.begin(),v.end());
    int link[node+1],sz[node+1];
    for(int i=1;i<=node;i++)
    {
        link[i]=i;
        sz[i]=1;
    }
    for(auto it:v)
    {
        tie(w,a,b)=it;
        if(finder(link,a)==finder(link,b))
            continue;
        final_tree.push_back(make_pair(a,b));
        final_weight+=w;
        join(a,b,link,sz);
    }
    cout<<endl;
    for(auto it:final_tree)
        cout<<it.first<<" "<<it.second<<endl;
    cout<<"final weight: "<<final_weight<<endl;
    return 0;
}


/*
6 8
1 2 3
1 5 5
2 3 5
2 5 6
3 4 9
3 6 3
4 6 7
5 6 2
*/
































/*
==========================================
All Longest path from nodes in tree
==========================================


#include<bits/stdc++.h>
using namespace std;
tuple<int,int,int>  f_smax[10];
int dfs_tree(int node,int prev,vector<int> v[],int dis[])
{
    int fmax=0,smax=0,child=0;
    for(int i : v[node])
    {
        if(i==prev)
            continue;
        int depth=1+dfs_tree(i,node,v,dis);
        if(fmax<depth)
        {
            smax=fmax;
            fmax=depth;
            child=i;
        }
        else if(smax<depth)
            smax=depth;
    }
    f_smax[node]=make_tuple(fmax,smax,child);
    return dis[node]=fmax;
}

void par_path(int node,int prev,vector<int> v[],int dis[])
{
    int fmax,smax,child;
    for(int i:v[node])
    {
        if(i==prev)
            continue;
        tie(fmax,smax,child)=f_smax[node];
        if(child==i)
        {
            if(1+smax>dis[i])
            {
                dis[i]=1+smax;
                f_smax[i]=make_tuple(1+smax,dis[i],node);
            }
        }
        else if(1+fmax>dis[i])
        {
            dis[i]=1+fmax;
            f_smax[i]=make_tuple(1+fmax,dis[i],node);
        }
        par_path(i,node,v,dis);
    }
}


int main()
{
    int nodes,edges,a,b;
    cout<<"Enter nodes and edges"<<endl;
    cin>>nodes>>edges;
    vector<int> v[nodes+1];
    int dis[nodes+1];
    cout<<"Enter edges"<<endl;
    for(int i=0;i<edges;i++)
    {
        cin>>a>>b;
        v[a].push_back(b);
        v[b].push_back(a);    // undirected
    }
    for(int i=1;i<=nodes;i++)
        dis[i]=0;
    //fillup
    dfs_tree(1,0,v,dis);
    par_path(1,0,v,dis);

    for(int i=1;i<=nodes;i++)
        cout<<dis[i]<<" ";
    cout<<endl;
    return 0;
}

*/









/*
======================================================================
Constructing tree from inorder and preorder  && inorder and postorder
======================================================================

#include<bits/stdc++.h>
using namespace std;
int nodes;
unordered_map<int,int> um;
queue<int> q;
struct node
{
    int data;
    node * left;
    node * right;
    node(int d)
    {
        data=d;
        left=NULL;right=NULL;
    }
};

void post_order(node * root)
{
    if(root==NULL)
        return;
    post_order(root->left);
    post_order(root->right);
    cout<<root->data<<" ";
}
void pre_order(node * root)
{
    if(root==NULL)
        return;
    cout<<root->data<<" ";
    pre_order(root->left);
    pre_order(root->right);
}
void in_order(node * root)
{
    if(root==NULL)
        return;
    in_order(root->left);
    cout<<root->data<<" ";
    in_order(root->right);
}

node * build_tree(int l,int r)
{
    if(q.empty())
        return NULL;
    int par=q.front();
    q.pop();
    node *tp=new node(par);
    if(q.empty())
        return tp;
    int curpar_pos=um[par],child_pos=um[q.front()];
    if(child_pos>=l && child_pos<curpar_pos)
        tp->left=build_tree(l,curpar_pos-1);
    child_pos=um[q.front()];
    if(child_pos>curpar_pos && child_pos<=r)
        tp->right=build_tree(curpar_pos+1,r);
    return tp;
}

node * build_treepost(int l,int r)
{
    if(q.empty())
        return NULL;
    int par=q.front();
    q.pop();
    node *tp=new node(par);
    if(q.empty())
        return tp;
    int curpar_pos=um[par],child_pos=um[q.front()];
    if(child_pos>curpar_pos && child_pos<=r)
        tp->right=build_treepost(curpar_pos+1,r);
    child_pos=um[q.front()];
    if(child_pos>=l && child_pos<curpar_pos)
        tp->left=build_treepost(l,curpar_pos-1);
    return tp;
}

void reverseQueue(queue<int>& Queue)
{
    stack<int> Stack;
    while (!Queue.empty()) {
        Stack.push(Queue.front());
        Queue.pop();
    }
    while (!Stack.empty()) {
        Queue.push(Stack.top());
        Stack.pop();
    }
}


int main()
{
    cout<<"Enter nodes"<<endl;
    cin>>nodes;
    int in,pre[nodes+1];
    while(!q.empty())
        q.pop();
    cout<<"Enter inorder and preorder"<<endl;
    for(int i=1;i<=nodes;i++)
    {
        cin>>in;
        um[in]=i;
    }
    for(int i=1;i<=nodes;i++)
    {
        cin>>in;
        q.push(in);
    }
    // if we have postorder reverse the queue and we'll get the tree
    //reverseQueue(q);
    //node * tree=build_treepost(1,nodes);            // inorder and postorder
    node * tree=build_tree(1,nodes);                  // inorder and preorder
    post_order(tree);
    return 0;
}

*/




















/*
==================================================
Diameter of the tree
==================================================


#include<bits/stdc++.h>
using namespace std;
int ans;
int dfs_tree(int node,int prev,vector<int> v[])
{
    int fmax=0,smax=-1;
    for(int i : v[node])
    {
        if(i==prev)
            continue;
        int depth=1+dfs_tree(i,node,v);
        if(fmax<depth)
        {
            smax=fmax;
            fmax=depth;
        }
        else if(smax<depth)
            smax=depth;
    }
    if(smax==-1 && ans<fmax)
        ans=fmax;
    else if(fmax+smax>ans)
        ans=fmax+smax;
    return fmax;
}

int main()
{
    int nodes,edges,a,b;
    cout<<"Enter nodes and edges"<<endl;
    cin>>nodes>>edges;
    vector<int> v[nodes+1];
    cout<<"Enter edges"<<endl;
    for(int i=0;i<edges;i++)
    {
        cin>>a>>b;
        v[a].push_back(b);
        v[b].push_back(a);    // undirected
    }
    ans=-1;
    int tp=dfs_tree(1,0,v);
    cout<<ans<<endl;
    return 0;
}




DFS approach will be first run  a dfs from any node and reach the farthest node you can reach.
From there again run a DFS and get the farthest node. This will be the diameter.
WHY? It helps shape the tree. The diameter will be a horizontal line and rest nodes will be hanging on it.


*/































/*
=================================================
Count the numnber of nodes in eachsubtree
=================================================



#include<bits/stdc++.h>
using namespace std;
void count_subtrees(int n,int p,vector<int> v[],int count_t[])   //p-> previous node
{
    count_t[n]=1;
    for(int i=0;i<v[n].size();i++)
    {
        if(v[n][i]==p)
            continue;
        count_subtrees(v[n][i],n,v,count_t);
        count_t[n]+=count_t[v[n][i]];
    }
}

int main()
{
    int nodes,edges,a,b;
    cout<<"enter nodes and edges"<<endl;
    cin>>nodes>>edges;
    vector<int> v[nodes+1];
    int count_t[nodes+1];
    cout<<"enter edges"<<endl;
    for(int i=0;i<edges;i++)
    {
        cin>>a>>b;
        v[a].push_back(b);
        v[b].push_back(a);
    }
    count_subtrees(1,0,v,count_t);
    for(int i=1;i<=nodes;i++)
        cout<<count_t[i]<<" ";
    cout<<endl;
    return 0;
}

*/






























/*
==============================================================
Dijkstras (Single source shortest path to all other nodes
==============================================================
// Greedy (carefully examines the path and the path where we have reached is the final path( because it does not work
  for negative edge weight


#include<iostream>
#include<queue>
#include<vector>
#include<algorithm>
using namespace std;
int main()
{
    int edges,nodes,a,b,w;
    cout<<"Enter the number of nodes and edges"<<endl;
    cin>>nodes>>edges;
    vector<pair<int,int>> v[nodes+1];  //adj list
    int vis[nodes+1],dis[nodes+1];
    cout<<"Enter edges with weight"<<endl;
    for(int i=0;i<edges;i++)
    {
        cin>>a>>b>>w;
        v[a].push_back(make_pair(b,w));
        v[b].push_back(make_pair(a,w));       //undirected
    }
    priority_queue<pair<int,int>> q;  // weight and node
    //source node in queue
    q.push(make_pair(0,1));
    for(int i=1;i<=nodes;i++)
    {
        dis[i]=1000;  // inf
        vis[i]=0;
    }
    dis[1]=0;
    while(!q.empty())
    {
        int a=q.top().second;
        q.pop();
        if(vis[a]==1)
            continue;
        vis[a]=1;
        for(int i=0;i<v[a].size();i++)
        {
            int b=v[a][i].first,w=v[a][i].second;
            if(dis[a]+w<dis[b])
            {
                dis[b]=dis[a]+w;
                q.push(make_pair(-1*dis[b],b));   //negative dis because we have max p_queue as default
            }
        }
    }
    for(int i=1;i<=nodes;i++)
        cout<<dis[i]<<" ";
    cout<<endl;
    return 0;
}
*/






















/*
==================================================================================
Floyd Warshal
(All nodes shortest path)
==================================================================================
//Key idea take every node as the intermediate node b/w 2 nodes and see if it can minimize the distance

#include<iostream>
using namespace std;
int main()
{
    int nodes,edges,x,y,w;
    cout<<"Enter number of nodes and edges"<<endl;
    cin>>nodes>>edges;
    int a[nodes+1][nodes+1];

    cout<<"Enter the edges with their weight"<<endl;
    for(int i=1;i<=nodes;i++)
    {
        for(int j=1;j<=nodes;j++)
        {
            if(i==j)
                a[i][j]=0;    // no cost to reach to the same node
            else
                a[i][j]=10000;   // inf
        }
    }
    for(int i=0;i<edges;i++)   // populating the 2d matrix where there is a direct edge
    {
        cin>>x>>y>>w;
        a[x][y]=w;
        a[y][x]=w;              //undirected
    }
    for(int k=1;k<=nodes;k++)  // keeping every node as intermediate node b/w 2 node i j
    {
        for(int i=1;i<=nodes;i++)
        {
            for(int j=1;j<=nodes;j++)
                a[i][j]=min(a[i][j],a[i][k]+a[k][j]);
        }
    }
    for(int i=1;i<=nodes;i++)
    {
        for(int j=1;j<=nodes;j++)
            cout<<a[i][j]<<" ";
        cout<<endl;
    }
    return 0;
}
*/


























/*
================================================================================
(BellmanFord)
Single Source Shortest path to all vertices (can also have neagtive edge lenght)
================================================================================


#include<iostream>
#include<tuple>
#include<vector>
using namespace std;
int main()
{
    int edges,nodes,a,b,w;
    vector<tuple<int,int,int>> e;   // edge representaion of weighted graph (a,b,w) edge from a to b having weight w
    cout<<"Enter nodes and edges"<<endl;
    cin>>nodes>>edges;
    int dis[nodes+1];
    cout<<"Enter weighted edges"<<endl;
    for(int i=0;i<edges;i++)
    {
        cin>>a>>b>>w;
        e.push_back(make_tuple(a,b,w));
    }
    for(int i=1;i<=nodes;i++)
        dis[i]=INT_MAX;
    dis[1]=0;
    for(int i=0;i<nodes-1;i++)              //longest path will have length atmost n-1 (no repetition no cycles)
    {
        for(int i=0;i<e.size();i++)         // keep on looking at the edges as long as the distance can be minimized
        {
            int aa,bb,ww;
            tie(aa,bb,ww)=e[i];
            if(dis[bb]>dis[aa]+ww)
                dis[bb]=dis[aa]+ww;
        }
    }
    for(int i=1;i<=nodes;i++)
        cout<<dis[i]<<" ";
    cout<<endl;
    return 0;
}


*/






/*
======================================================================
======================================================================
======================================================================
======================================================================


GRAPHS


======================================================================
======================================================================
======================================================================
======================================================================
======================================================================
======================================================================
*/

























/*
=============================================================================================
We have n persons having weights. Lift with max holding capicity x. Minimum rounds needed so thata
everyone reaches top floor.
============================================================================================
// Permuting through all the persons will work but will be slow. Reduce it to subsets with DP.



#include<iostream>
#include<utility>
#include<algorithm>
using namespace std;
int main()
{
    int wt[]={2,3,3,5,6},x=10,n=5;
    pair<int,int> best[1<<n];
    best[0]={1,0};
    for(int s=1;s<(1<<n);s++)
    {
        best[s]={n+1,0};
        for(int p=0;p<n;p++)
        {

            if(s & (1<<p))
            {
                auto options=best[s^ (1<<p)];
                if(options.second+wt[p]<=x)  // can we accomodate the person
                    options.second+=wt[p];
                else                        // can't accomodate take another lift for him
                {
                    options.first++;
                    options.second=wt[p];
                }
                best[s]=min(best[s],options);
            }

        }
    }
    for(int i=0;i<1<<n;i++)
    {
        cout<<best[i].first<<" "<<best[i].second<<" ";
        cout<<endl;
    }
    //cout<<best[1<<n].first<<endl;
    return 0;
}
*/





















/*
==========================================================================================
Given k products and their prices along n days. We want to purchase all the items and we can
only purchase 1 item in a day. What is the minimum cost in doing so?
===========================================================================================


#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;
int a[][8]={{6,9,5,2,8,9,1,6},
    {8,2,6,2,7,5,7,2},
    {5,3,9,7,3,5,1,4}};
const int days=8,prod_num=3;
int memo[days][1<<prod_num];
int recur(int i,int sett)
{
    if(sett==0)
        return 0;
    else if(i<0)
        return 10000;
    else
    {
        if(memo[i][sett]!=-1)
            return memo[i][sett];
        else
        {
            int minn=10000;
            for(int q=0;q<prod_num;q++)
            {
                if(sett & (1<<q))
                {
                    sett=sett & ~(1<<q);
                    minn=min(minn,recur(i-1,sett)+a[q][i]);
                    sett=sett | (1<<q);
                }
            }
            return memo[i][sett]=min(minn,recur(i-1,sett));
        }
    }
}

int main()
{
    int sett=(1<<prod_num)-1;
    for(int i=0;i<days;i++)
    {
        for(int j=0;j<=sett;j++)
            memo[i][j]=-1;
    }
    cout<<recur(7,sett);
    return 0;
}


















#include<iostream>
#include<algorithm>
using namespace std;
int main()
{
    //price of products along the days
    int a[][8]={{6,9,5,2,8,9,1,6},
    {8,2,6,2,7,5,7,2},
    {5,3,9,7,3,5,1,4}};
    const int days=8,prod_num=3; // prod_num : Total number of products
    int memo[1<<prod_num][days];        // Try to buy the ith subset in the dth day in the memo array
    for(int i=0;i<1<<prod_num;i++)
    {
        for(int j=0;j<days;j++)
        {
            if(i==0)
                memo[i][j]=0;
            else
                memo[i][j]=10000;
        }
    }
    for(int i=0;i<prod_num;i++)     // on first day we can only buy one product of the following price
        memo[1<<i][0]=a[i][0];
    for(int d=1;d<days;d++)     //days
    {
        for(int s=0;s<(1<<prod_num) ;s++)//subsets
        {
            memo[s][d]=memo[s][d-1];
            for(int k=0;k<prod_num;k++)
            {
                if(s & (1<<k))
                {
                    memo[s][d]=min(memo[s][d],
                                   memo[s^(1<<k)][d-1]+a[k][d]);   // flip the kth bit take rest of the subset from day -1 and the flipped bit from this day only
                }
            }
        }
    }
    for(int i=0;i<1<<prod_num;i++)
    {
        for(int j=0;j<days;j++)
            cout<<memo[i][j]<<" ";
        cout<<endl;
    }
    return 0;
}





*/






























/*


====================================================================
====================================================================
SEGMENT TREE
====================================================================
====================================================================

#include<iostream>
using namespace std;
const int n=8;
int a[]={5,8,6,3,2,7,2,6},seg[2*n+2];

void build(int node,int start,int endd)
{
    if(start==endd)                 // base case reached leaf node of seg tree
        seg[node]=a[start];
    else                            // build recursively
    {
        int mid=(start+endd+1)/2;
        build(2*node,start,mid-1);
        build(2*node+1,mid,endd);
        seg[node]=seg[2*node]+seg[2*node+1];               // how we want to make the seg tree (summ of ranges)
    }
}

int query(int node ,int start,int endd , int l , int r)
{
    if(l>endd || r<start)        // out of range return nothing
        return 0;
    if(l<=start && r>=endd)         // falls completely in the range
        return seg[node];
    else                            //falls partially in the range
    {
        int mid=(start+endd+1)/2;
        int s1=query(2*node,start,mid-1,l,r);
        int s2=query(2*node+1,mid,endd,l,r);
        return s1+s2;
    }
}

int main()
{
    build(1,0,7);
    for(int i=1;i<2*n+1;i++)
        cout<<seg[i]<<" ";
    cout<<endl;
    cout<<query(1,0,7,5,7);
    return 0;
}






#include<iostream>
using namespace std;
const int n=8;
int a[]={5,8,6,3,2,7,2,6},seg[2*n+1];   // 2*n as n is power of 2 else it will take more space 2*n+1

void build()
{
    for(int i=0;i<=2*n;i++)
        seg[i]=0;
    for(int i=0;i<n;i++)
        seg[i+n]=a[i];    // leaf node starts with n
    int k=n;
    for(k/=2;k>=1;k/=2)
    {
        for(int i=k;i<k+k;i++)
            seg[i]=seg[2*i]+seg[2*i+1];
    }
}

void update_add(int index,int value)
{
    int k=index+n;
    seg[k]+=value;
    for(k/=2;k>=1;k/=2)
        seg[k]=seg[2*k]+seg[2*k+1];
}

int query(int l,int r)
{
    int a=l+n,b=r+n;
    int sum=0;
    while(a<=b)
    {
        if(a%2==1) sum+=seg[a++];                   // adding it if it is not present in the above level
        if(b%2==0) sum+=seg[b--];
        a/=2;b/=2;
    }
    return sum;
}

int main()
{
    build();
    for(int i=1;i<2*n+1;i++)
        cout<<seg[i]<<" ";
    cout<<endl;
    cout<<query(1,3);
    return 0;
}



*/
























/*


====================================================================
====================================================================
FENWIK TREE (BINARY INDEXED TREE)
====================================================================
====================================================================



#include<iostream>
using namespace std;
const int n=8;
int a[]={-111,1,3,4,8,6,1,4,2},BIT[n+1];   // -111 for making it 1 indexed array

void update(int index, int value)
{
    for(;index<=n;index+=(index & -index))
        BIT[index]+=value;
}

int summ(int index)
{
    int sum=0;
    for(;index>0;index-=(index & -index))
        sum+=BIT[index];
    return sum;
}

int main()
{
    //Basic idea => store the partial sums at indexes (indexes can be represented as powers of 2)

    // -x gives the 2's complement in bits
    // x & (-x)  gives the last set bit               //1 1 0 1 0
                                                           // ^
                                                          //  |

    for(int i=1;i<=n;i++)
        update(i,a[i]);
    for(int i=1;i<=n;i++)
        cout<<BIT[i]<<" ";
    cout<<endl;
    cout<<summ(5)<<endl;
    return 0;
}
*/



















/*
==================================
Sliding window minimum
==================================

#include<iostream>
#include<list>
using namespace std;
int main()
{
    list<int> q;
    int a[]={2,1,4,5,3,4,1,2},n=8,k=4;              //(k)window size
    for(int i=0;i<k;i++)
    {
        while(!q.empty() && q.back()>a[i])
        {q.pop_back();}
        q.push_back(a[i]);
    }
    cout<<q.front()<<" ";
    for(int i=k;i<n;i++)
    {
        if(q.front()==a[i-k])
            q.pop_front();
        while(!q.empty() && q.back()>a[i])
        {q.pop_back();}
        q.push_back(a[i]);
        cout<<q.front()<<" ";
    }
    return 0;
}



*/



















/*
============================================
Subarray sum equals to some  number x
============================================

#include<iostream>
using namespace std;
int main()
{
    int a[]={1,3,2,5,1,1,2,3},sum=8,n=8;
    int i=0,j=0,tpsum=0;
    while(i<n)                                                               // two pointers moving in the same direction
    {
        for(;j<n;j++)
        {
            tpsum+=a[j];
            if(tpsum==sum)
                break;
            if(tpsum>sum)
            {
                while(tpsum>sum)
                {
                    tpsum-=a[i];
                    i++;
                }
            }
        }
        if(tpsum==sum)
            break;
    }
    for(int q=i;q<=j;q++)
        cout<<a[q]<<" ";
    cout<<endl;
    return 0;
}


*/











/*
=====================================
LIS(Longest Increasing Subsequence)
=====================================

#include<iostream>
using namespace std;
int main()
{
    int a[]={10, 22, 9, 33, 21, 50, 41, 60, 80},n=9,maxx=-1;
    //int a[]={6,2,5,1,7,4,8,3},n=8,maxx=-1;
    for(int i=0;i<n;i++)
    {
        int cal=1,prev=a[i];
        for(int j=i+1;j<n;j++)
        {
            if(a[j]>prev)
            {
                cal+=1;
                prev=a[j];
            }
        }
        if(cal>maxx)
            maxx=cal;
    }
    cout<<maxx;
    return 0;
}
*/





/*
=========================================
EDIT Distance
===========================================
#include<iostream>
#include<string>
using namespace std;
string s1="love",s2="movie";
int n1,n2;
int edit_dist(int i ,int j)
{
    if(i==n1 && j==n2)
        return 0;
    else if(i==n1 && j!=n2)
        return n2-j;
    else if(i!=n1 && j==n2)
        return n1-i;
    else
    {
        if(s1[i]==s2[j])
            return edit_dist(i+1,j+1);
        else
            return min(1+edit_dist(i,j+1),   // insert
                       min(1+edit_dist(i+1,j+1),        //edit
                           1+edit_dist(i+1,j)));             //delete
    }

}
int main()
{
    n1=s1.size();n2=s2.size();
    cout<<edit_dist(0,0);
}





#include<iostream>
#include<string>
#include<algorithm>
using namespace std;
string s1="love",s2="movie";
int n1,n2;
int main()
{
    n1=s1.size()+1;n2=s2.size()+1;
    int memo[n1][n2];
    for(int i=0;i<n1;i++)
    {
        for(int j=0;j<n2;j++)
        {
            if(i==0)
                memo[i][j]=j;
            else if(j==0)
                memo[i][j]=i;
            else
            {
                if(s1[i-1]==s2[j-1])
                    memo[i][j]=memo[i-1][j-1];
                else
                    memo[i][j]=min(1+memo[i-1][j-1],min(1+memo[i-1][j],1+memo[i][j-1]));
            }
        }
    }
    for(int i=0;i<n1;i++)
    {
        for(int j=0;j<n2;j++)
            cout<<memo[i][j]<<" ";
        cout<<endl;
    }
    cout<<memo[n1-1][n2-1];
}

*/










/*
=====================
01 Knapsack
=====================

#include<iostream>
#include<algorithm>
using namespace std;
int val[]={60,100,120},wt[]={10,20,30};
const int W=50,n=3;
int memo[n][W];
int knap_01(int i,int w)
{
    if(i>=n)
        return 0;
    else
    {
        if(memo[i][w]!=-1)
            return memo[i][w];
        else
        {
            if(w+wt[i]<=W)
                return memo[i][w]=max(knap_01(i+1,w),val[i]+knap_01(i+1,w+wt[i]));
            else
                return memo[i][w]=knap_01(i+1,w);
        }
    }

}

int main()
{
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<W;j++)
            memo[i][j]=-1;
    }
    cout<<knap_01(0,0);
    return 0;
}













#include<iostream>
#include<algorithm>
using namespace std;
int main()
{
    int val[]={60,100,120},wt[]={10,20,30},W=50,n=3;
    int memo[n+1][W+1]={0};
    for(int i=0;i<=n;i++)
    {
        for(int j=0;j<=W;j++)
        {
            if(i==0 || j==0)
                memo[i][j]=0;
            else if(j-wt[i-1]>=0)
                memo[i][j]=max(val[i-1]+memo[i-1][j-wt[i-1]],memo[i-1][j]);
            else
                memo[i][j]=memo[i-1][j];
        }
    }
    cout<<memo[n][W];
    return 0;
}



*/

















/*
==================================================================
Knapsack (all the sums that you can make using the following coins)
==================================================================


#include<iostream>
using namespace std;
int main()
{
    int a[]={1,3,3,5},sum_of_all=12,n=4;
    // either i take a coin or i don't take it
    // possible to make a sum if i end up(take some coins subtract that from the sum) at 0 (base case 0 can be made by using no coins)
    int possible[sum_of_all+1][n+1]={0};
    for(int j=0;j<=n;j++)
        possible[0][j]=1;
    for(int i=1;i<sum_of_all+1;i++)
    {
        for(int j=1;j<=n;j++)
        {
            if(i-a[j-1]>=0)
                possible[i][j] |= possible[i-a[j-1]][j-1];            //take it
            possible[i][j] |= possible[i][j-1];                        //leave it
        }
    }
    for(int i=1;i<sum_of_all+1;i++)
    {
        for(int j=0;j<=n;j++)
        {
            if(possible[i][j]==1)
            {
                cout<<i<<" ";
                break;
            }
        }
    }
    return 0;
}







#include<iostream>
using namespace std;
int main()
{
    int a[]={1,3,3,5},sum_of_all=12,n=4;
    int memo[sum_of_all+1]={0};
    memo[0]=1;   //can make 0 sum if we don't take any coin
    for(int i=0;i<n;i++)    // build up the answer with 0 coins then 1 coin then 2 coin ..... with all coins
    {
        for(int j=sum_of_all;j>=0;j--)
        {
            if(memo[j]==1)
                memo[j+a[i]]=1;
        }
    }
    for(int i=0;i<=sum_of_all;i++)
    {
        if(memo[i]==1)
            cout<<i<<" ";
    }
    return 0;
}


*/






















/*
=============================================================
Max sum from top left to bottom right in a matrix
=============================================================



#include<iostream>
#include<algorithm>
using namespace std;
int n;
int max_sum(int a[][5],int i,int j)                                                    // Can also memoize this
{
    if(i==n-1 && j==n-1)
        return a[i][j];
    else if(i+1<n && j+1<n)
        return a[i][j]+max(max_sum(a,i+1,j),max_sum(a,i,j+1));
    else if(i+1<n && j+1>=n)
        return a[i][j]+max_sum(a,i+1,j);
    else
        return a[i][j]+max_sum(a,i,j+1);
}

int main()
{
    int a[][5]={{3,7,9,2,7},{9,8,3,5,5},{1,7,9,8,5},{3,8,6,4,10},{6,3,9,7,8}};
    n=5;
    cout<<max_sum(a,0,0);
    return 0;
}

/*#include<iostream>
#include<algorithm>
using namespace std;
int main()
{
    int a[][5]={{3,7,9,2,7},{9,8,3,5,5},{1,7,9,8,5},{3,8,6,4,10},{6,3,9,7,8}};
    int n=5;
    for(int i=1;i<n;i++)
    {
        a[i][0]+=a[i-1][0];
        a[0][i]+=a[0][i-1];
    }
    for(int i=1;i<n;i++)                                                // we can reach  a tile from above or from it's left
    {                                                                   // SO optimize till there (subproblem) then take the max of up/left
        for(int j=1;j<n;j++)
            a[i][j]+=max(a[i-1][j],a[i][j-1]);
    }
    cout<<a[n-1][n-1];
    return 0;
}
*/
































/*
================================================================
All the possible solutions to form the sum X using coins
================================================================

#include<iostream>
#include<vector>
using namespace std;

int main()
{
    int x=5,memo[100];
    vector<int> v={1,3,4};
    memo[0]=1;
    for(int i=1;i<=x;i++)
    {
        memo[i]=0;
        for(int j=0;j<v.size();j++)
        {
            if(i-v[j]>=0)
                memo[i]+=memo[i-v[j]];
        }
    }
    cout<<memo[x];
    return 0;
}

*/
















/*
==================================================================
Min coins needed to form a sum X
==================================================================

#include<iostream>
#include<algorithm>
#include<vector>
using namespace std;
vector<int> v;
int memo[100];

int min_coins(int sum,vector<int> v)
{
    if(memo[sum]!=-1)
        return memo[sum];
    else
    {
        if(sum==0)
            return memo[0]=0;
        else
        {
            int ans=1000;//int max
            for(int i=0;i<v.size();i++)
            {
                if(sum-v[i]>=0)
                    ans=min(ans,1+min_coins(sum-v[i],v));
            }
            return memo[sum]=ans;
        }
    }

}

int main()
{
    v={1,3,4};
    int x=35;
    for(int i=0;i<100;i++)
        memo[i]=-1;
    cout<<min_coins(x,v);
    return 0;
}


*/







/*
#include<iostream>
#include<vector>
using namespace std;
int main()
{
    vector<int> v={1,3,4};                  // if x= 6 ans=2 can't get that with greedy? use DP
    int x=6,memo[100],first[100];
    memo[0]=0;first[0]=0;
    for(int i=1;i<=x;i++)
    {
        memo[i]=1000;//int max
        for(int j=0;j<v.size();j++)
        {
            if(i-v[j]>=0)
            {
                if(1+memo[i-v[j]]<memo[i])
                {
                    memo[i]=1+memo[i-v[j]];
                    first[i]=v[j];
                }
            }
        }
    }
    cout<<memo[x]<<endl;
    while(x!=0)
    {
        cout<<first[x]<<" ";
        x-=first[x];
    }
    return 0;
}

*/


















/*

================================================
Huffman coding
================================================

#include<iostream>
#include<queue>
#include<string>
#include<unordered_map>
using namespace std;
unordered_map<string,string> ans;
struct H_Tree
{
    int sum;
    string data;
    struct H_Tree *left=NULL;                             // can have pointer of the same struct(defined space it will take)
    struct H_Tree *right=NULL;                             // but can't take struct itself as inner struct then another inner and so on ,so space is not defined not complete (compilation error)
    H_Tree(int s,string d)
    {
        sum=s;
        data=d;
        left=NULL;
        right=NULL;
    }
};

struct CompareTrees
{
    bool operator ()(H_Tree *const& t1 , H_Tree *const& t2)
    {
        return ((*t1).sum>(*t2).sum);
    }
};

void huffman_code(H_Tree t,string s)
{
    if(t.left==NULL && t.right==NULL)
        ans[t.data]=s;
    else
    {
        if(t.left!=NULL)
            huffman_code(*(t.left),s+"0");
        if(t.right!=NULL)
            huffman_code(*(t.right),s+"1");
    }
}
void traverse(H_Tree t)
{
    if(t.left==NULL && t.right==NULL)
        cout<<t.data<<endl;
    else
    {
        if(t.left!=NULL)
            traverse(*(t.left));
        if(t.right!=NULL)
            traverse(*(t.right));
    }
}
int main()
{
    string s="aabacdaca";
    unordered_map<string,int> m;
    priority_queue<H_Tree *,vector<H_Tree *>,CompareTrees> q;
    for(int i=0;i<s.size();i++)
    {
        string stp;
        stp.push_back(s[i]);
        if(m.find(stp)==m.end())
            m[stp]=1;
        else
            m[stp]++;
    }
    auto it=m.begin();
    for(int i=0;it!=m.end();it++)
    {
        H_Tree *temp=new H_Tree((*it).second,(*it).first);
        q.push(temp);
    }
    while(q.size()!=1)
    {
        H_Tree *t1=q.top();q.pop();
        H_Tree *t2=q.top();q.pop();
        H_Tree *temp=new H_Tree((*t1).sum+(*t2).sum,(*t1).data+(*t2).data);
        if((*t1).sum<=(*t2).sum)
        {
            (*temp).left=t1;
            (*temp).right=t2;
        }
        else
        {
            (*temp).left=t2;
            (*temp).right=t1;
        }
        q.push(temp);
    }
    H_Tree *temp=q.top();
    //traverse(*temp);

    cout<<(*temp).data<<endl;
    cout<<(*((*temp).left)).data<<endl;
    cout<<(*((*temp).right)).data<<endl;
    cout<<(*((*((*temp).left)).left)).data<<endl;

    huffman_code(*temp,"");
    for(auto it:ans)
        cout<<it.first<<" "<<it.second<<endl;


    return 0;
}


*/


















/*
============================================================================================================
Grid NxN how many ways from top left to bottome down taking each cell atmost once.
//7x7=111712
//Can I optimize more?
==============================================================================================================



#include<iostream>
#include<vector>
using namespace std;
int n,ct,flag=0;
void paths(vector<vector<int>> v,int i,int j)
{
        if(i==n-1 && j==n-1)                                                //bottom right reached before visiting others
        {
            int flag=1;
            for(int i=0;i<n;i++)
            {
                for(int j=0;j<n;j++)
                {
                    if(v[i][j]==0)
                    {
                        flag=0;
                        break;
                    }
                }
                if(flag==0)
                    break;
            }
            if(flag==1)
                ct++;
            else
                return;
        }
        else
        {
            //walls leave unvisited cells on left/right side of the wall!

            if(i==0 && v[i+1][j]==1)        // up wall
            {
                if(j-1>=0 && j+1<n && v[i][j-1]==0 && v[i][j+1]==0)
                    return;
            }
            if(i+1==n && v[i-1][j]==1)      //down wall
            {
                if(j-1>=0 && j+1<n && v[i][j-1]==0 && v[i][j+1]==0)
                    return;
            }
            if(j==0 && v[i][j+1]==1)        //left wall
            {
                if(i+1<n && i-1>=0 && v[i+1][j]==0 && v[i-1][j]==0)
                    return;
            }
            if(j+1==n && v[i][j-1]==1)        //right wall
            {
                if(i+1<n && i-1>=0 && v[i+1][j]==0 && v[i-1][j]==0)
                    return;
            }



            if(i+1<n && v[i+1][j]==1 && i-1>=0 && v[i-1][j]==1)       //down between wall
            {
                if(j-1>=0 && j+1<n && v[i][j-1]==0 && v[i][j+1]==0)
                    return;
            }
            if(i-1>=0 && v[i-1][j]==1 && i+1<n && v[i+1][j]==1)      //up between wall
            {
                if(j-1>=0 && j+1<n && v[i][j-1]==0 && v[i][j+1]==0)
                    return;
            }


            if(j+1<n && v[i][j+1]==1 && j-1>=0 && v[i][j-1]==1)       //right between wall
            {
                if(i+1<n && i-1>=0 && v[i+1][j]==0 && v[i-1][j]==0)
                    return;
            }
            if(j-1>=0 && v[i][j-1]==1 && j+1<n && v[i][j+1]==1)      //left between wall
            {
                if(i+1<n && i-1>=0 && v[i+1][j]==0 && v[i-1][j]==0)
                    return;
            }



            if(i+1<n && v[i+1][j]==0)       //down
            {
                v[i+1][j]=1;
                paths(v,i+1,j);
                v[i+1][j]=0;
            }
            if(i-1>=0 && v[i-1][j]==0)      //up
            {
                v[i-1][j]=1;
                paths(v,i-1,j);
                v[i-1][j]=0;
            }
            if(j+1<n && v[i][j+1]==0)       //right
            {
                v[i][j+1]=1;
                paths(v,i,j+1);
                v[i][j+1]=0;
            }
            if(j-1>=0 && v[i][j-1]==0)      //left
            {
                v[i][j-1]=1;
                paths(v,i,j-1);
                v[i][j-1]=0;
            }
        }
}
int main()
{
    cin>>n;
    vector<vector<int>> v(n,vector<int>(n));
    ct=0;
    v[0][0]=1;v[1][0]=1;
    paths(v,1,0);
    cout<<2*ct<<endl;               // can go down or right but we have symmetry so we can multiply by 2 and only go right/down
    return 0;
}


*/










/*

=================================================
NQueens
==================================================





#include<iostream>
#include<vector>
using namespace std;
int n,ct=0,chosen[16],hesh[16];
vector<int> per;
vector<vector<int>> board(4);

void choose(int idx,int y_n)
{
    int i=idx/n,j=idx%n;
    chosen[board[i][j]]+=y_n;
    for(int k=j-1;k>=0;k--)       //left
        chosen[board[i][k]]+=y_n;
    for(int k=j+1;k<n;k++)           //right
        chosen[board[i][k]]+=y_n;
    for(int k=i-1;k>=0;k--)           //up
        chosen[board[k][j]]+=y_n;
    for(int k=i+1;k<n;k++)           //down
        chosen[board[k][j]]+=y_n;
    for(int k=i-1,l=j-1;k>=0 && l>=0;k--,l--)           //up left diag
            chosen[board[k][l]]+=y_n;
    for(int k=i-1,l=j+1;k>=0 && l<n;k--,l++)           //up right diag
            chosen[board[k][l]]+=y_n;
    for(int k=i+1,l=j-1;k<n && l>=0;k++,l--)           //down left diag
            chosen[board[k][l]]+=y_n;
    for(int k=i+1,l=j+1;k<n && l<n;k++,l++)           //down right diag
            chosen[board[k][l]]+=y_n;
}

void per_nqueens()
{
    if(per.size()==n)
    {
        int flag=1;
        for(int q=0;q<per.size();q++)
        {
            if(hesh[per[q]]==0)
            {
                flag=0;
                break;
            }
        }
        if(flag==0)
        {
            ct++;
            for(int q=0;q<per.size();q++)
            {
                hesh[per[q]]=1;
                cout<<per[q]<<" ";
            }
            cout<<endl;
        }
    }
    for(int i=0;i<16;i++)
    {
        if(chosen[i]>=1)
            continue;
        else
        {
            choose(i,1);
            per.push_back(i);
            per_nqueens();
            choose(i,-1);
            per.pop_back();
        }
    }
}
int main()
{
    n=4;
    int counter=0;
    for(int i=0;i<16;i++)
    {
        chosen[i]=0;
        hesh[i]=0;
    }
    for(int i=0;i<4;i++)
    {
        for(int j=0;j<4;j++)
        {
            board[i].push_back(counter);
            counter++;
        }
    }
    /*choose(1,1);
    for(int i=0;i<16;i++)
    {
        if(chosen[i]==0)
            cout<<i<<" ";
    }
    cout<<endl;
    choose(7,1);
    for(int i=0;i<16;i++)
    {
        if(chosen[i]==0)
            cout<<i<<" ";
    }
    cout<<endl;
    choose(8,1);
    for(int i=0;i<16;i++)
    {
        if(chosen[i]==0)
            cout<<i<<" ";
    }
    cout<<endl;
*/
/*
    per_nqueens();
    cout<<endl<<ct<<" possible ways";

    return 0;
}







/*
#include<iostream>
#include<vector>
using namespace std;
vector<int> column(100),diag1(100),diag2(100),perm;
int n,ct=0;
void nqueens_book(int y)
{
    if(perm.size()==n)
    {
        ct++;
        for(int i=0;i<perm.size();i++)
            cout<<perm[i]<<" ";
        cout<<endl;
    }
    else
    {
        for(int x=0;x<n;x++)
        {
            if(column[x]==1 || diag1[x+y]==1 || diag2[x-y+n-1]==1)
                continue;
            else
            {
                column[x]=diag1[x+y]=diag2[x-y+n-1]=1;
                perm.push_back(n*y+x);
                nqueens_book(y+1);
                perm.pop_back();
                column[x]=diag1[x+y]=diag2[x-y+n-1]=0;
            }
        }
    }
}
int main()
{
    n=4;
    nqueens_book(0);
    cout<<ct<<endl;
    return 0;
}



*/















/*
================================================
Permutation
================================================

#include<iostream>
#include<vector>
#include<string>
using namespace std;

vector<int> perms;
int chosen[10];
void permutation_book(vector<int> v)
{
    if(perms.size()==v.size())
    {
        for(int q=0;q<perms.size();q++)
            cout<<perms[q]<<" ";
        cout<<endl;
    }
    else
    {
        for(int i=0;i<v.size();i++)
        {
            if(chosen[i]==1)
                continue;
            else
            {
                chosen[i]=1;
                perms.push_back(v[i]);
                permutation_book(v);
                chosen[i]=0;
                perms.pop_back();
            }
        }
    }
}

void permutation(vector<int> v,vector<int> tp={})
{
    if(v.empty())
    {
        for(int q=0;q<tp.size();q++)
            cout<<tp[q]<<" ";
        cout<<endl;
    }
    else
    {
        for(int i=0;i<v.size();i++)
        {
            vector<int> temp(v);
            temp.erase(temp.begin()+i);
            tp.push_back(v[i]);
            permutation(temp,tp);
            tp.pop_back();
        }
    }
}

int main()
{
    vector<int> v={1,2,3};
    permutation(v);
    cout<<endl;
    permutation_book(v);
    return 0;
}


*/









/*
==================================================
Subsets
==================================================

1) Recursion


#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;
vector<int> v;
void subsets(int a[],int i)
{
    if(i>=3)
    {
        for(int i=0;i<v.size();i++)
            cout<<v[i]<<" ";
        cout<<endl;
    }
    else
    {
        subsets(a,i+1);
        v.push_back(a[i]);
        subsets(a,i+1);
        v.pop_back();
    }
}
int main()
{
    int a[]={0,1,2};
    vector<int> tp;
    subsets(a,0);
    return 0;
}
*/




/*
2) Bits
#include<iostream>
#include<math.h>
using namespace std;
int main()
{
    int a[]={0,1,2},n=3;
    for(int i=0;i<(1<<n);i++)           // 2^n
    {
        for(int j=0;j<n;j++)            //check if jth bit is set if yes take it.
        {
            if(i & (1<<j))
                cout<<a[j]<<" ";
        }
        cout<<endl;
    }
    return 0;
}
*/







/*
================================================================================
Sorting needs comparison operator for user defined struct OR comparison function
=================================================================================

#include<iostream>
#include<algorithm>
using namespace std;
struct P
{
    int x,y;
    bool operator < (P p)
    {
        if(p.x!=x)
            return x<p.x;
        else
            return y<p.y;
    }
};
bool comp(const P p1, const P p2)            .// comparison function should not modify the argument passed that's why const used
{
    if(p1.x!=p2.x)
        return p1.x<p2.x;
    else
        return p1.y<p2.y;
}
int main()
{
    P p1,p2;
    p1.x=2;p1.y=3;
    p2.x=1;p2.y=2;
    vector<P> v;
    v.push_back(p1);
    v.push_back(p2);
    for(auto it =v.begin();it!=v.end();it++)
        cout<<(*it).x<<" "<<(*it).y<<endl;
    sort(v.begin(),v.end(),comp);
    for(auto it =v.begin();it!=v.end();it++)
        cout<<(*it).x<<" "<<(*it).y<<endl;
    return 0;
}

*/











/*
=======================================
Kadanes Maximum contiguous subarray sum
========================================

#include<iostream>
#include<algorithm>
using namespace std;
int main()
{
    int a[]={-1,2,4,-3,5,2,-5,2};
    int max_overall=0,max_tillhere=0;
    for(int i=0;i<8;i++)
    {
        max_tillhere+=a[i];
        if(max_tillhere<0)
            max_tillhere=0;
        max_overall=max(max_overall,max_tillhere);
    }
    cout<<max_overall<<endl;
    return 0;
}

*/

