# CMake generated Testfile for 
# Source directory: /root/uwb_ws/src/nlink_parser
# Build directory: /root/uwb_ws/build/nlink_parser
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_nlink_parser_gtest_nlink_parser_test "/root/uwb_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python3" "/opt/ros/noetic/share/catkin/cmake/test/run_tests.py" "/root/uwb_ws/build/test_results/nlink_parser/gtest-nlink_parser_test.xml" "--return-code" "/root/uwb_ws/devel/lib/nlink_parser/nlink_parser_test --gtest_output=xml:/root/uwb_ws/build/test_results/nlink_parser/gtest-nlink_parser_test.xml")
set_tests_properties(_ctest_nlink_parser_gtest_nlink_parser_test PROPERTIES  _BACKTRACE_TRIPLES "/opt/ros/noetic/share/catkin/cmake/test/tests.cmake;160;add_test;/opt/ros/noetic/share/catkin/cmake/test/gtest.cmake;98;catkin_run_tests_target;/opt/ros/noetic/share/catkin/cmake/test/gtest.cmake;37;_catkin_add_google_test;/root/uwb_ws/src/nlink_parser/CMakeLists.txt;195;catkin_add_gtest;/root/uwb_ws/src/nlink_parser/CMakeLists.txt;0;")
subdirs("extern/serial")
