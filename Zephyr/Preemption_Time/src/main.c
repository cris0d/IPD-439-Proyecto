#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>

static const struct gpio_dt_spec lpt_pin =
	GPIO_DT_SPEC_GET(DT_PATH(zephyr_user), task1_gpios);
static const struct gpio_dt_spec hpt_pin =
	GPIO_DT_SPEC_GET(DT_PATH(zephyr_user), task2_gpios);

#define STACK_SIZE 512
#define PRIORITY_HPT 4   /* equivalente a osPriorityAboveNormal */
#define PRIORITY_LPT 5   /* equivalente a osPriorityNormal */

K_THREAD_STACK_DEFINE(taskHPT_stack, STACK_SIZE);
K_THREAD_STACK_DEFINE(taskLPT_stack, STACK_SIZE);

static struct k_thread taskHPT_data;
static struct k_thread taskLPT_data;

K_SEM_DEFINE(sem_preemption, 0, 1);

/* Equivalente a StartTaskHPT */
void StartTaskHPT(void *p1, void *p2, void *p3)
{
	while (1) {
		k_sem_take(&sem_preemption, K_FOREVER);
		gpio_pin_set_dt(&hpt_pin, 1);
		gpio_pin_set_dt(&hpt_pin, 0);
	}
}

/* Equivalente a StartTaskLPT */
void StartTaskLPT(void *p1, void *p2, void *p3)
{
	while (1) {
		gpio_pin_set_dt(&lpt_pin, 1);
		k_sem_give(&sem_preemption);
		gpio_pin_set_dt(&lpt_pin, 0);
		k_yield();
	}
}

int main(void)
{
	gpio_pin_configure_dt(&lpt_pin, GPIO_OUTPUT_INACTIVE);
	gpio_pin_configure_dt(&hpt_pin, GPIO_OUTPUT_INACTIVE);

	k_thread_create(&taskHPT_data, taskHPT_stack, STACK_SIZE,
			StartTaskHPT, NULL, NULL, NULL,
			PRIORITY_HPT, 0, K_NO_WAIT);

	k_thread_create(&taskLPT_data, taskLPT_stack, STACK_SIZE,
			StartTaskLPT, NULL, NULL, NULL,
			PRIORITY_LPT, 0, K_NO_WAIT);

	return 0;
}