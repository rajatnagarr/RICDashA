#!/bin/bash

encoded_lua_script="RVZBTCAibG9jYWwgYWxsX2tleXMgPSByZWRpcy5jYWxsKCdLRVlTJywgJyonKTsgbG9jYWwgcmVzdWx0cyA9IHt9OyBmb3IgaSwga2V5IGluIGlwYWlycyhhbGxfa2V5cykgZG8gbG9jYWwgdHlwZSA9IHJlZGlzLmNhbGwoJ1RZUEUnLCBrZXkpLm9rOyBpZiB0eXBlID09ICdzdHJpbmcnIHRoZW4gdGFibGUuaW5zZXJ0KHJlc3VsdHMsIHtrZXksICdzdHJpbmcnLCByZWRpcy5jYWxsKCdHRVQnLCBrZXkpfSkgZWxzZWlmIHR5cGUgPT0gJ2xpc3QnIHRoZW4gbG9jYWwgbGlzdF92YWx1ZXMgPSByZWRpcy5jYWxsKCdMUkFOR0UnLCBrZXksIDAsIC0xKTsgdGFibGUuaW5zZXJ0KHJlc3VsdHMsIHtrZXksICdsaXN0JywgdGFibGUuY29uY2F0KGxpc3RfdmFsdWVzLCAnLCAnKX0pIGVsc2VpZiB0eXBlID09ICdzZXQnIHRoZW4gbG9jYWwgc2V0X21lbWJlcnMgPSByZWRpcy5jYWxsKCdTTUVNQkVSUycsIGtleSk7IHRhYmxlLmluc2VydChyZXN1bHRzLCB7a2V5LCAnc2V0JywgdGFibGUuY29uY2F0KHNldF9tZW1iZXJzLCAnLCAnKX0pIGVsc2VpZiB0eXBlID09ICdoYXNoJyB0aGVuIGxvY2FsIGhhc2hfZmllbGRzID0gcmVkaXMuY2FsbCgnSEdFVEFMTCcsIGtleSk7IGxvY2FsIGhhc2hfc3RyID0gJyc7IGZvciBqID0gMSwgI2hhc2hfZmllbGRzLCAyIGRvIGhhc2hfc3RyID0gaGFzaF9zdHIgLi4gaGFzaF9maWVsZHNbal0gLi4gJzonIC4uIGhhc2hfZmllbGRzW2ogKyAxXSAuLiAnLCAnOyBlbmQgdGFibGUuaW5zZXJ0KHJlc3VsdHMsIHtrZXksICdoYXNoJywgaGFzaF9zdHJ9KSBlbHNlaWYgdHlwZSA9PSAnenNldCcgdGhlbiBsb2NhbCB6c2V0X21lbWJlcnMgPSByZWRpcy5jYWxsKCdaUkFOR0UnLCBrZXksIDAsIC0xLCAnV0lUSFNDT1JFUycpOyBsb2NhbCB6c2V0X3N0ciA9ICcnOyBmb3IgaiA9IDEsICN6c2V0X21lbWJlcnMsIDIgZG8genNldF9zdHIgPSB6c2V0X3N0ciAuLiB6c2V0X21lbWJlcnNbal0gLi4gJygnIC4uIHpzZXRfbWVtYmVyc1tqICsgMV0gLi4gJyksICc7IGVuZCB0YWJsZS5pbnNlcnQocmVzdWx0cywge2tleSwgJ3pzZXQnLCB6c2V0X3N0cn0pIGVuZCBlbmQ7IHJldHVybiByZXN1bHRzIiAw"

kubectl exec -n ricplt -it statefulset-ricplt-dbaas-server-0 -- /bin/sh -c "
cd /usr/local/bin &&
echo \"$encoded_lua_script\" | base64 -d | ./redis-cli"

: << 'END'
In this script, you use kubectl exec to run commands inside a specific pod of a Kubernetes cluster 
(statefulset-ricplt-dbaas-server-0 in the ricplt namespace). 

The commands executed are:

Change the directory to /usr/local/bin.
Decode the Lua script from its base64 encoded form.
Execute the decoded Lua script using redis-cli.
The Lua script itself interacts with a Redis database to retrieve all of the data in the database 

Original lua script:

EVAL "local all_keys = redis.call('KEYS', '*'); local results = {}; for i, key in ipairs(all_keys) do local type = redis.call('TYPE', key).ok; if type == 'string' then table.insert(results, {key, 'string', redis.call('GET', key)}) elseif type == 'list' then local list_values = redis.call('LRANGE', key, 0, -1); table.insert(results, {key, 'list', table.concat(list_values, ', ')}) elseif type == 'set' then local set_members = redis.call('SMEMBERS', key); table.insert(results, {key, 'set', table.concat(set_members, ', ')}) elseif type == 'hash' then local hash_fields = redis.call('HGETALL', key); local hash_str = ''; for j = 1, #hash_fields, 2 do hash_str = hash_str .. hash_fields[j] .. ':' .. hash_fields[j + 1] .. ', '; end table.insert(results, {key, 'hash', hash_str}) elseif type == 'zset' then local zset_members = redis.call('ZRANGE', key, 0, -1, 'WITHSCORES'); local zset_str = ''; for j = 1, #zset_members, 2 do zset_str = zset_str .. zset_members[j] .. '(' .. zset_members[j + 1] .. '), '; end table.insert(results, {key, 'zset', zset_str}) end end; return results" 0

Due to the quotes in the command, it could not be directly put in to the bash script, so I had to encode it into base 64.
I used this command in a linux shell to get the encoded version of the text

echo -n 'EVAL "local all_keys = redis.call('KEYS', '*'); local results = {}; for i, key in ipairs(all_keys) do local type = redis.call('TYPE', key).ok; if type == 'string' then table.insert(results, {key, 'string', redis.call('GET', key)}) elseif type == 'list' then local list_values = redis.call('LRANGE', key, 0, -1); table.insert(results, {key, 'list', table.concat(list_values, ', ')}) elseif type == 'set' then local set_members = redis.call('SMEMBERS', key); table.insert(results, {key, 'set', table.concat(set_members, ', ')}) elseif type == 'hash' then local hash_fields = redis.call('HGETALL', key); local hash_str = ''; for j = 1, #hash_fields, 2 do hash_str = hash_str .. hash_fields[j] .. ':' .. hash_fields[j + 1] .. ', '; end table.insert(results, {key, 'hash', hash_str}) elseif type == 'zset' then local zset_members = redis.call('ZRANGE', key, 0, -1, 'WITHSCORES'); local zset_str = ''; for j = 1, #zset_members, 2 do zset_str = zset_str .. zset_members[j] .. '(' .. zset_members[j + 1] .. '), '; end table.insert(results, {key, 'zset', zset_str}) end end; return results" 0' | base64
END
