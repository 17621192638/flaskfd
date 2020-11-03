/*
 Navicat Premium Data Transfer

 Source Server         : 本地
 Source Server Type    : MySQL
 Source Server Version : 80020
 Source Host           : 127.0.0.1:3306
 Source Schema         : test

 Target Server Type    : MySQL
 Target Server Version : 80020
 File Encoding         : 65001

 Date: 03/11/2020 09:34:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '用户表',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `company_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '企业名称',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  `status` int(0) NULL DEFAULT 0 COMMENT '-1 禁用 0 启用',
  `user_type` int(0) NOT NULL DEFAULT 3 COMMENT '1 超级管理员 2 企业母账户 3 企业子账户',
  `nickname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户昵称',
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '手机号',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `avatar_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `phone_status` int(0) NULL DEFAULT 0 COMMENT '-1 验证失败 0 未验证 1 验证成功',
  `phone_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '手机验证码',
  `email_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `email_status` int(0) NULL DEFAULT NULL COMMENT '-1 验证失败 0 未验证 1 验证成功',
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注字段',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 45 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, '2020-07-25 10:25:03', 'admin', 'admin', '超级管理员', '2020-11-02 14:16:15', 0, 1, '超管', '', '', '', NULL, '', '', NULL, '超级管理员');
INSERT INTO `user` VALUES (45, '2020-11-02 14:32:58', '张三', '111', '张三有限公司', '2020-11-02 14:32:58', 0, 3, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL);
INSERT INTO `user` VALUES (46, '2020-11-02 14:33:09', '李四', '111', '李四有限公司', '2020-11-02 14:33:09', 0, 3, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL);
INSERT INTO `user` VALUES (47, '2020-11-02 14:33:24', '王五', '111', '王五有限公司', '2020-11-02 14:33:24', 0, 3, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL);
INSERT INTO `user` VALUES (48, '2020-11-02 14:33:45', 'admin2', 'admin', 'test', '2020-11-02 14:33:45', 0, 3, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL);

SET FOREIGN_KEY_CHECKS = 1;
