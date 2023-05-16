/*
 * @创建文件时间: 2021-06-01 22:41:21
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-06-05 01:03:36
 * 联系Qq:1638245306
 * @文件介绍: 角色管理接口
 */
import { request } from "@/api/service";

export const urlPrefix = "/api/system/sensory_alerts/";

export function sendAlerts() {
  return request({
    url: urlPrefix+"send_email_alerts",
    method: "get",
  });
}

