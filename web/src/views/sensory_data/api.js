/*
 * @创建文件时间: 2021-06-01 22:41:21
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-06-05 01:03:36
 * 联系Qq:1638245306
 * @文件介绍: 角色管理接口
 */

import { request } from "@/api/service";
export const urlPrefix = "/api/system/sensory_data/";

export function GetList(query, range_search = undefined) {
  if (range_search) {
    return request({
      url: urlPrefix + "get_data_within_range/",
      method: "get",
      params: { ...query },
    });
  } else {
    return request({
      url: urlPrefix,
      method: "get",
      params: { ...query },
    });
  }
}

export function GetObj(obj) {
  return request({
    url: urlPrefix + obj.id + "/",
    method: "get",
  });
}

export function createObj(obj) {
  return request({
    url: urlPrefix,
    method: "post",
    data: obj,
  });
}

export function UpdateObj(obj) {
  return request({
    url: urlPrefix + obj.id + "/",
    method: "put",
    data: obj,
  });
}

export function DelObj(id) {
  return request({
    url: urlPrefix + id + "/",
    method: "delete",
    data: { id },
  });
}

const downloadFile = function ({ url, params, method, filename = "Export_" }) {
  request({
    url: url,
    method: method,
    params: params,
    responseType: "blob",
    // headers: {Accept: 'application/vnd.openxmlformats-officedocument'}
  }).then((res) => {
    const xlsxName = window.decodeURI(
      res.headers["content-disposition"].split("=")[1]
    );
    const fileName = xlsxName || `${filename}.xlsx`;
    if (res) {
      const blob = new Blob([res.data], { type: "charset=utf-8" });
      const elink = document.createElement("a");
      elink.download = fileName;
      elink.style.display = "none";
      elink.href = URL.createObjectURL(blob);
      document.body.appendChild(elink);
      elink.click();
      URL.revokeObjectURL(elink.href); // 释放URL 对象0
      document.body.removeChild(elink);
    }
  });
};

export function exportData(params) {
  return downloadFile({
    url: urlPrefix + "export_data/",
    params: params,
    method: "get",
  });
}
