"""初始化种子数据 —— 首次运行时填充示例数据"""
from database import SessionLocal, engine, Base
from security import hash_password
import models


def init():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 如果已有数据则跳过
    if db.query(models.User).first():
        print("✅ 数据已存在，跳过初始化")
        db.close()
        return

    print("🐱 正在初始化种子数据...")

    # ── 用户 ──
    admin = models.User(username="admin", password_hash=hash_password("admin123"),
                        nickname="超级管理员🐾", avatar="👩‍💻", role="admin")
    catfan = models.User(username="catfan", password_hash=hash_password("cat123"),
                         nickname="北华喂猫第一人", avatar="😻", role="certified")
    demo = models.User(username="demo", password_hash=hash_password("demo123"),
                       nickname="路过的同学", avatar="🧑‍🎓", role="user")
    db.add_all([admin, catfan, demo])
    db.flush()

    # ── 猫猫 ──
    cats_data = [
        dict(name="橘座",emoji="😺",color="#FF8C00",gender="♂ 公",age="3岁",
             fur="橘色虎斑",neutered=True,status="在校",area="一食堂门口",
             personality=["友善亲人","贪吃","爱撒娇"],vaccine=True,deworm=True,
             description="北华第一网红猫，十橘九胖的典范代表。"),
        dict(name="花花",emoji="😽",color="#E91E63",gender="♀ 母",age="2岁",
             fur="三花色",neutered=True,status="在校",area="图书馆花园",
             personality=["害羞","安静","偶尔高冷"],vaccine=True,deworm=True,
             description="图书馆旁的安静女孩，喜欢趴在花坛边晒太阳。"),
        dict(name="小黑",emoji="🐈‍⬛",color="#424242",gender="♂ 公",age="4岁",
             fur="纯黑色",neutered=True,status="在校",area="工学院楼下",
             personality=["独立","高冷","夜行侠"],vaccine=True,deworm=True,
             description="神出鬼没的校园保安猫，深夜巡逻主力。"),
        dict(name="大白",emoji="😸",color="#90CAF9",gender="♂ 公",age="1岁",
             fur="纯白色",neutered=False,status="待收养",area="南门小花园",
             personality=["粘人","活泼","话唠"],vaccine=True,deworm=False,
             description="超级粘人的小可爱，正在等待一个温暖的家。"),
        dict(name="三花姐",emoji="😻",color="#AB47BC",gender="♀ 母",age="5岁",
             fur="三花色",neutered=True,status="在校",area="二食堂后门",
             personality=["温柔","大姐大","母性强"],vaccine=True,deworm=True,
             description="校园猫中的大姐大，经常护着新来的小猫。"),
        dict(name="灰灰",emoji="😿",color="#78909C",gender="♀ 母",age="6岁",
             fur="蓝灰色",neutered=True,status="已收养",area="原: 行政楼前",
             personality=["沉稳","温顺","佛系"],vaccine=True,deworm=True,
             description="已被教职工收养，偶尔回学校探亲。"),
    ]
    cat_objs = []
    for cd in cats_data:
        cat = models.Cat(**cd)
        db.add(cat)
        cat_objs.append(cat)
    db.flush()

    # ── 事件 ──
    events = [
        models.CatEvent(cat_id=cat_objs[0].id, event_date="2022-03-15",
                        event_type="🔍 发现", description="在一食堂附近首次被发现"),
        models.CatEvent(cat_id=cat_objs[0].id, event_date="2022-04-20",
                        event_type="✂️ 绝育", description="完成绝育手术"),
        models.CatEvent(cat_id=cat_objs[0].id, event_date="2022-05-10",
                        event_type="💉 疫苗", description="完成三联疫苗接种"),
    ]
    db.add_all(events)

    # ── 关系 ──
    db.add(models.CatRelation(
        cat_id=cat_objs[0].id, related_cat_id=cat_objs[3].id,
        related_cat_name="大白", relation_type="好朋友"))

    # ── 评论 ──
    db.add(models.Comment(user_id=catfan.id, cat_id=cat_objs[0].id,
                          content="橘座今天又胖了！太可爱啦～", likes=12))

    # ── 投喂 ──
    db.add(models.Feeding(user_id=catfan.id, cat_id=cat_objs[0].id,
                          location="一食堂门口", food="猫粮+小鱼干"))

    # ── 公告 ──
    db.add(models.Announcement(author_id=admin.id, title="🎄 冬季投喂指南",
           content="冬季来临，请大家在投喂点增加温水供应。投喂时间建议在早7点和晚5点。"))

    db.commit()
    db.close()
    print("✅ 种子数据初始化完成！")


if __name__ == "__main__":
    init()