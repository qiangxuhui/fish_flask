from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from mapp.models.gift import Gift
from . import web

__author__ = '七月'


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    """
    1. 获取当前索要的礼物的信息
    2. 自己不能向自己请求书籍 is_yourself_gift
    3. 鱼豆必须足够（大于等于1）
    4. 每次索取一本书自己必须送出一本书
    """
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你自己的，不能向自己索要书籍')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)

    gifter = current_gift.user.summary
    return render_template('drift.html', gifter=gifter, beans=current_user.beans)


@web.route('/pending')
def pending():
    pass


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    pass


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    pass


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    pass
