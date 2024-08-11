#include <opencv2/opencv.hpp>
#include <opencv2/xfeatures2d.hpp>
#include <iostream>

int main() {
    // 读取图像
    cv::Mat img = cv::imread("../../maps/UI_MapBack_-1_-1.png");
    if (img.empty()) {
        std::cerr << "Could not open or find the image!" << std::endl;
        return -1;
    }

    // 转换为灰度图像
    cv::Mat img_gray;
    cv::cvtColor(img, img_gray, cv::COLOR_BGR2GRAY);

    // 创建 SURF 检测器
    cv::Ptr<cv::xfeatures2d::SURF> surf = cv::xfeatures2d::SURF::create();
    std::vector<cv::KeyPoint> surf_keypoints;
    cv::Mat surf_des;

    // 检测和计算特征点
    surf->detectAndCompute(img_gray, cv::noArray(), surf_keypoints, surf_des);
    std::cout << surf_keypoints.size() << std::endl;

    // 绘制特征点
    cv::Mat img_keypoints, img_onlykp;
    cv::drawKeypoints(img, surf_keypoints, img_keypoints, cv::Scalar::all(-1), cv::DrawMatchesFlags::DRAW_RICH_KEYPOINTS);
    cv::drawKeypoints(img, surf_keypoints, img_onlykp, cv::Scalar::all(-1), cv::DrawMatchesFlags::NOT_DRAW_SINGLE_POINTS);

    // 显示图像
    cv::imshow("surf", img_keypoints);
    cv::imshow("surf_onlykp", img_onlykp);

    // 分块处理
    std::vector<std::pair<int, int>> dircs = {
        {-1, -1}, {-1, 0}, {-1, 1},
        {0, -1}, {0, 0}, {0, 1},
        {1, -1}, {1, 0}, {1, 1}
    };
    int L = 128;

    int row = img_gray.rows;
    int col = img_gray.cols;
    std::cout << row << ", " << col << std::endl;

    for (int rb = 0; rb < row; rb += L) {
        for (int cb = 0; cb < col; cb += L) {
            cv::Mat img_block = img_gray(cv::Rect(cb, rb, L, L));
            cv::Mat img_block_neibor = cv::Mat::zeros(3 * L, 3 * L, CV_8U);
            cv::Mat img_block_neibor_mask = cv::Mat::zeros(3 * L, 3 * L, CV_8U);

            // 检测和计算特征点
            surf->detectAndCompute(img_block, cv::noArray(), surf_keypoints, surf_des);
            for (auto& kp : surf_keypoints) {
                kp.pt.x += cb;
                kp.pt.y += rb;
            }

            // 绘制特征点
            cv::Mat img_block_keypoints, img_block_onlykp;
            cv::drawKeypoints(img, surf_keypoints, img_block_keypoints, cv::Scalar::all(-1), cv::DrawMatchesFlags::DRAW_RICH_KEYPOINTS);
            cv::drawKeypoints(img, surf_keypoints, img_block_onlykp, cv::Scalar::all(-1), cv::DrawMatchesFlags::NOT_DRAW_SINGLE_POINTS);

            // 显示图像
            cv::imshow("block", img_block_keypoints);
            cv::imshow("block_onlykp", img_block_onlykp);
            cv::waitKey(0);
        }
    }

    cv::waitKey(0);
    return 0;
}