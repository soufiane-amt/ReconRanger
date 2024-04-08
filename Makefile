TMP_RES_DIR=./tmp_results/
TOOL_RES_DIR=./tools_extracted_result/

all: clean

clean:
	@rm -rf ${TMP_RES_DIR}*
	@rm -rf ${TOOL_RES_DIR}*
	@rm -f *.txt *.log
	@rm -fr 2024*
