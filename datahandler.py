import uuid
import datetime
from typing import List, Any


def newbase():
    global id_ref
    id_ref = []


async def datahandle(team, id):
    await cleandata()
    proof = await prüfedata(team)
    if proof:
        return proof
    await newdata(team, id)
    return False


async def cleandata():
    now = datetime.datetime.utcnow()
    for i in id_ref:
        delta = now - i[0]
        delta_sec = delta.seconds
        if delta_sec > 14400:
            id_ref.remove(i)


async def prüfedata(team):
    for i in id_ref:
        print(i)
        if i[1] == team:
            return i[2]
    return False


async def newdata(team, id):
    now = datetime.datetime.utcnow()
    newline = [now, team, id]
    id_ref.append(newline)